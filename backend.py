from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from database import db
from typing import Optional

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="static")
