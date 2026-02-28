from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import db
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.helpers import generate_random_string
import checklist as checklist_module
#matplotlib for graph
import matplotlib
matplotlib.use('Agg') # must be non interactive backend 
import matplotlib.pyplot as plt
import io, base64
import loan_list as loan_list_module
from typing import Optional

BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

print("KINDE_CLIENT_ID:", os.getenv("KINDE_CLIENT_ID"))
print("KINDE_HOST:", os.getenv("KINDE_HOST"))

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-change-me"),
    same_site="lax",
    https_only=False,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

oauth = OAuth(
    client_id=os.getenv("KINDE_CLIENT_ID"),
    client_secret=os.getenv("KINDE_CLIENT_SECRET"),
    host=os.getenv("KINDE_HOST"),
    redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
)

def get_current_user(request: Request):
    user = request.session.get("kinde_user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

<<<<<<< HEAD
# Holden's function for creating matplotlib bar graph
# used https://matplotlib.org as a resource
def generate_loan_chart(loans):
    if not loans:
        return None

    names = [loan[2] for loan in loans]          # loan_name
    principals = [loan[6] for loan in loans]     # p_amount
    min_payments = [loan[3] for loan in loans]   # min_payment

    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.barh(names, principals, color='#4A90D9', label='Total Principal')
    ax.barh(names, min_payments, color='#27AE60', label='Min Payment')

    ax.set_xlabel('Amount ($)')
    ax.set_title('Loan Payoff Progress')
    ax.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.get("/login")
async def login(request: Request):
    url = await oauth.login()
    return RedirectResponse(url=url, status_code=302)

@app.get("/register")
async def register(request: Request):
    url = await oauth.register()
    return RedirectResponse(url=url, status_code=302)

@app.get("/callback")
async def callback(request: Request, code: str, state: str | None = None):
    user_id = state or generate_random_string(16)
    result = await oauth.handle_redirect(code=code, user_id=user_id, state=None)

    user = result.get("user", {})
    user["_kinde_user_id"] = user_id

    # Sync Kinde user into your DB
    name = f"{user.get('given_name', '')} {user.get('family_name', '')}".strip()
    email = user.get("email", "")
    db_user_id = db.insert_user(name, email, None)  # won't duplicate if they've logged in before
    user["db_user_id"] = db_user_id

    request.session["kinde_user"] = user
    return RedirectResponse(url="/", status_code=302)

@app.get("/logout")
async def logout(request: Request):
    user = request.session.get("kinde_user")
    user_id = user.get("_kinde_user_id") if user else None
    request.session.clear()
    logout_url = await oauth.logout(
        user_id=user_id,
        logout_options={"post_logout_redirect_uri": os.getenv("LOGOUT_REDIRECT_URL")}
    )
    # Override the SDK-generated URL and force the correct param name
    from urllib.parse import urlencode
    params = {
        "client_id": os.getenv("KINDE_CLIENT_ID"),
        "post_logout_redirect_uri": os.getenv("LOGOUT_REDIRECT_URL")
    }
    logout_url = f"{os.getenv('KINDE_HOST')}/logout?{urlencode(params)}"
    print("LOGOUT URL:", logout_url)
    return RedirectResponse(url=logout_url, status_code=302)
# ----- goal modifications -----
@app.post("/goal_create")
async def goal_create(
    request: Request, 
    goal: str = Form(...),
    duration: int = Form(...),
    status: Optional[str] = Form(None)
    ): 
    current_user = request.session.get("kinde_user")
    db_user_id = current_user.get("db_user_id")  # use db_user_id not kinde_id
    status_flag = 1 if status == 'yes' else 0
    db.add_goal(db_user_id, status_flag, goal, duration)
    return RedirectResponse(url="/", status_code=302)

@app.post("/goal_status")
async def toggle_goal_status(
    request: Request, 
    goal_id: int = Form(...),
    current_status: int = Form(...)
):
    current_user = request.session.get("kinde_user")
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    # Flip the status: 0 becomes 1, anything else (like 1) becomes 0
    new_status = 1 if current_status == 0 else 0
    
    db.update_goal_status(goal_id, new_status, current_user.get("id"))
    
    return RedirectResponse(url="/", status_code=302)

@app.post("/delete_goal")
async def delete_goal(
    request: Request,
    goal_id: str = Form(...)
):
    db.delete_goal(goal_id)
    return RedirectResponse(url="/", status_code=302)

# ------ loan modifications ------
@app.post("/loan_create")
async def loan_create(
    request: Request,
    loan_name: str = Form(...),
    min_payment: float = Form(...),
    loan_type: str = Form(...),
    late_fee: float = Form(...),
    p_amount: float = Form(...),
    ir: float = Form(...),
    it: str = Form(...),
    term_length: int = Form(...),
    amount_payed: float = Form(0.0)
):
    current_user = request.session.get("kinde_user")
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    kinde_id = current_user.get("id")
    db.create_loan(kinde_id, loan_name, min_payment, loan_type, late_fee, p_amount, ir, it, term_length, amount_payed)
    return RedirectResponse(url="/", status_code=302)
# ------ home page ------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    current_user = request.session.get("kinde_user")

    if "state" in request.query_params:
        return RedirectResponse(url="/", status_code=302)

    # Secure Gatekeeper
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)

    # Access the user's unique ID from the Kinde session
    kinde_id = current_user.get("id")
    if not kinde_id:
        # If Kinde didn't return an ID, the session might be corrupted
        request.session.clear()
        return RedirectResponse(url="/login")

    # Get loans and generate chart
    db_user_id = current_user.get("db_user_id")
    loans = db.get_loans(db_user_id)
    chart = generate_loan_chart(loans)

    # Initialize your checklist with the authenticated user
    checklist = checklist_module.Checklist(current_user)
    goals = checklist.Create_Post()

    # get loans and loan summary data
    loans = loan_list_module.LoanList(current_user.get("id"))
    loan_summary = loans.Create_Post()

    return templates.TemplateResponse(
        "dashboard.jinja",
        {
            "request": request, 
            "user": current_user, 
            "goals": goals,
            "loan_summary": loan_summary
        }
    )

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)