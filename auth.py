import json
from dataclasses import dataclass

from authlib.integrations.starlette_client import OAuth


@dataclass
class Client:
    client_id: str
    client_secret: str
    server_metadata_url: str
    session_secret: str

with open("./env/secrets.json") as secrets:
    client = Client(**json.load(secrets))

oauth = OAuth()
oauth.register(
    name='authentik',
    client_id=client.client_id,
    client_secret=client.client_secret,
    # Das lässt uns basically openid benutzen. 
    # Sonst müssten wir API-URL, Token-URL und Authorize-URL angeben.
    server_metadata_url=client.server_metadata_url, 
    # goauthentik.io/api wird angegeben damit api im scope ist
    client_kwargs={'scope': 'openid email profile goauthentik.io/api'},
    )

def getOAuth():
    return oauth

def getSessionSecret():
    return client.session_secret
