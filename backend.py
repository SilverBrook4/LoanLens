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

load_dotenv()

BASE_DIR = Path(__file__).parent

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-change-me"),
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# initialize OAuth
kinde_oauth = OAuth(framework="fastapi", app=app)
# Tell FastAPI where to look for the Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def get_current_user(request: Request):
    # Check if a valid session exists
    if not kinde_oauth.is_authenticated():
        raise HTTPException(status_code=401, detail="Please log in first")
    
    # Get the user details directly from the SDK
    # This returns a dictionary with 'id', 'email', 'given_name', etc.
    user = kinde_oauth.get_user_details()
    return user

# WEB APP ROUTES
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "login.jinja",
        {"request": request,}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    # Access the user's unique ID from the Kinde token
    kinde_id = current_user.get("id")

    # Query your DB using ONLY this ID
    # example: user_data = db.query(User).filter(User.kinde_id == kinde_id).first()
    
    return templates.TemplateResponse(
        "dashboard.jinja", 
        {
            "request": request, 
            "user": current_user  # Pass the Kinde info to the frontend
        }
    )

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
