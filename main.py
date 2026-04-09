import base64
import json
from typing import Optional
from urllib.parse import urlparse

from authentik_client import User
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from auth import getOAuth, getSessionSecret
from dataprocessing.dataprocessing import (getProcessedUsers, getUserByPK,
                                           setUserByPK)

app = FastAPI()

# Der secret key hier ist um den session cookie mit dem frontend zu verifizieren. 
app.add_middleware(
    SessionMiddleware,
    secret_key=getSessionSecret(),
    same_site="lax",
    https_only=False,  # True in production
)

@app.get("/auth/login", description="Redirects the user to the login form for authentik (if not signed in already)")
async def login(request: Request, current_url: str):
    request.session.clear() 
    request.session["return_to"] = current_url
    ## Parse url because it comes with weird characters for certain symbols
    parsed = urlparse(current_url)
    frontend_origin = f"{parsed.scheme}://{parsed.netloc}"
    redirect_uri = f"{frontend_origin}/api/auth/callback"
    state = base64.urlsafe_b64encode(json.dumps({"return_to": current_url}).encode()).decode()                                                                             
    return await getOAuth().authentik.authorize_redirect(request, redirect_uri, state=state)

@app.get("/auth/callback", description="Stores session token in server-side session. Should redirect to original page")
async def callback(request: Request):
    token = await getOAuth().authentik.authorize_access_token(request)
    state = json.loads(base64.urlsafe_b64decode(request.query_params["state"]))                                                                                            
    request.session["access_token"] = token["access_token"]                                                                                                                
    return RedirectResponse(url=state["return_to"])     

@app.get("/users", description="Returns a list of users (todo: based on the current users view permissions)", response_model= list[User], response_model_exclude={"avatar", "uid", "uuid", "type", "path", "groups", "roles"})
async def getUsers(request: Request , attributes: Optional[str] = ''):   
    token = requireToken(request)
    users = getProcessedUsers(token, attributes)
    return users

@app.get("/users/{pk}", description="Returns a user based on identifier pk", response_model= User, response_model_exclude={"avatar", "uid", "uuid", "type", "path", "groups", "roles"})
async def getUser(request: Request , pk: int):   
    token = requireToken(request)
    users = getUserByPK(token, pk)
    return users

@app.post("/users/{pk}", description="", response_model= User, response_model_exclude={"avatar", "uid", "uuid", "type", "path", "groups", "roles"})
async def setUser(request: Request , pk: int, attributes: str = ''):  
    token = requireToken(request)
    users = setUserByPK(token, pk,attributes=json.loads(attributes))
    return users


def requireToken(request: Request):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail={"message": "Not authenticated"}
        )
    return str(token)