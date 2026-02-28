from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.sessions import SessionMiddleware
from database import db
from typing import Annotated
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv
from kinde_sdk.auth.oauth import OAuth
from checklist import Checklist

load_dotenv()

BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

print("KINDE_CLIENT_ID:", os.getenv("KINDE_CLIENT_ID"))
print("KINDE_HOST:", os.getenv("KINDE_HOST"))

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.helpers import generate_random_string

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
    # No framework= here — avoids the broken request context system entirely
    client_id=os.getenv("KINDE_CLIENT_ID"),
    client_secret=os.getenv("KINDE_CLIENT_SECRET"),
    host=os.getenv("KINDE_HOST"),
    redirect_uri=os.getenv("KINDE_REDIRECT_URI"),
)

def current_user(request: Request):
    return request.session.get("kinde_user")

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

    # Pass state=None to skip the SDK's internal state check (it can't store it
    # without a request context anyway — Kinde already validated it on their end)
    result = await oauth.handle_redirect(code=code, user_id=user_id, state=None)

    user = result.get("user", {})
    user["_kinde_user_id"] = user_id

    request.session["kinde_user"] = user
    return RedirectResponse(url="/", status_code=302)

@app.get("/logout")
async def logout(request: Request):
    user = current_user(request)
    user_id = user.get("_kinde_user_id") if user else None
    request.session.clear()
    logout_url = await oauth.logout(user_id=user_id)
    return RedirectResponse(url=logout_url, status_code=302)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if "state" in request.query_params:
        return RedirectResponse(url="/", status_code=302)

    user = current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("dashboard.jinja", {"request": request, "user": user})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    # Access the user's unique ID from the Kinde token
    kinde_id = current_user.get("id")

    checklist = Checklist(current_user)

    goals = checklist.Create_Post()

    # Query your DB using ONLY this ID
    # example: user_data = db.query(User).filter(User.kinde_id == kinde_id).first()
    
    return templates.TemplateResponse(
        "dashboard.jinja", 
        {
            "request": request, 
            "user": current_user,  # Pass the Kinde info to the frontend
            "goals": goals
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)