from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import db
from typing import Optional
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        "dashboard.jinja",
        {"request": request,}
    )

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
