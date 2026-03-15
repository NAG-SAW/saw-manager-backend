import json
from dataclasses import dataclass
from http.client import HTTPException

from auth import getOAuth
from dataprocessing.dataclasses import User

AUTHENTIK_URL = "auth.saw.rwth-aachen.de"

## Requests
async def getAllUsers(token: str, attributes: str) -> str:
    if not token:
        raise HTTPException(status_code=401)

    attributes = json.dumps(attributes)
    resp = await getOAuth().authentik.get(
        f"https://{AUTHENTIK_URL}/api/v3/core/users/?attributes={attributes}",
        token={"access_token": token, "token_type": "Bearer"}
    )
    return resp

## Hier sollte abhängig von Permissions andere Info angezeigt werden
def getUser(user_id: int) -> User | None:
    users = getAllUsers()
    print(f"Looking for user_id: {user_id}")
    print(f"Available users: {[u.User_ID for u in users]}")
    for user in users:
        if user.User_ID == user_id:
            return user
    return None
    # TODO add getUser functions based on permission -> use permission scopes from authentik




