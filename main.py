from http.client import HTTPException

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from auth import getOAuth, getSessionSecret
from dataprocessing.dataclasses import User
from dataprocessing.dataprocessing import getAllUsers

app = FastAPI()

# Der secret key hier ist um den session cookie mit dem frontend zu verifizieren. 
app.add_middleware(SessionMiddleware, secret_key=getSessionSecret())

@app.get("/")
def home(request: Request):
    return RedirectResponse(url=request.url_for("login"))

@app.get("/auth/login", description="Redirects the user to the login form for authentik (if not signed in already)")
async def login(request: Request):
    if request.session.get("user"):
        return RedirectResponse(url=request.url_for("getUsers"));
    
    redirect_uri = str(request.url_for("callback"))
    return await getOAuth().authentik.authorize_redirect(request, redirect_uri)

# Stattdessen sollte der user wieder auf der URL landen über die er zum login redirected wurde.
@app.get("/auth/callback", description="Stores session token in server-side session. Should redirect to original page")
async def callback(request: Request):
    token = await getOAuth().authentik.authorize_access_token(request)
    request.session["access_token"] = token["access_token"]
    return RedirectResponse(url=request.url_for("getUsers"))

@app.get("/users")
async def getUsers(request: Request, attributes: str) -> list[User]:   
    token = request.session.get("access_token") 
    return getAllUsers(token, attributes).json()
