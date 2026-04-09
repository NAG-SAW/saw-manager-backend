from typing import Any, Optional

import authentik_client
from authentik_client import UserRequest
from authentik_client.exceptions import ApiException
from authentik_client.models.user import User
from fastapi import HTTPException

AUTHENTIK_URL = "https://auth.saw.rwth-aachen.de/api/v3"

def getProcessedUsers(token: str, attributes: Optional[str]) -> list[User]: 
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")

    configuration = authentik_client.Configuration(
        host=AUTHENTIK_URL,
        access_token=token,
    )

    all_users = []
    page = 1

    with authentik_client.ApiClient(configuration) as api_client:
        api = authentik_client.CoreApi(api_client)

        ## Iterate over all available pages of users (authentik maxes out at 100 users page_size)
        while True:
            try:
                response = api.core_users_list(
                    page=page,
                    page_size=500,
                    attributes=attributes if attributes else None,
                )

                all_users.extend([user for user in response.results])

                if page >= response.pagination.total_pages:
                    break
                page += 1

            except ApiException as e:
                if(e.status):
                    raise HTTPException(status_code=e.status, detail=str(e))

    return all_users

def getUserByPK(token: str, pk: int) -> User | None:
    configuration = authentik_client.Configuration(
        host=AUTHENTIK_URL,
        access_token=token,
    )

    with authentik_client.ApiClient(configuration) as api_client:
        api = authentik_client.CoreApi(api_client)
        try:
            return api.core_users_retrieve(id=pk)
        except ApiException as e:
            if e.status:
                if e.status == 404:
                    raise HTTPException(status_code=404, detail="User not found")
                if e.status in (401, 403):
                    raise HTTPException(status_code=401, detail="Token invalid/expired")
                raise HTTPException(status_code=e.status, detail=str(e))
            
def setUserByPK(token: str, pk: int, attributes: dict[str, Any]) -> User | None:
    configuration = authentik_client.Configuration(
        host=AUTHENTIK_URL,
        access_token=token,
    )
    user = getUserByPK(token,pk)
    if(user):
        updateUserAttributes(user, attributes)
        with authentik_client.ApiClient(configuration) as api_client:
            api = authentik_client.CoreApi(api_client)
            try:
                return api.core_users_update(id=pk, user_request= UserRequest(**user.model_dump()))
            except ApiException as e:
                if e.status:
                    if e.status == 404:
                        raise HTTPException(status_code=404, detail="User not found")
                    if e.status in (401, 403):
                        raise HTTPException(status_code=401, detail="Token invalid/expired")
                    raise HTTPException(status_code=e.status, detail=str(e))
                

def updateUserAttributes(user: User, attributes: dict[str, Any]):
    user.attributes = attributes
            
