from typing import Optional

import authentik_client
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
                kwargs = {"page": page, "page_size": 500, 'attributes': ''}
                if attributes:
                    kwargs["attributes"] = attributes

                response = api.core_users_list(**kwargs)

                all_users.extend([user for user in response.results])

                if page >= response.pagination.total_pages:
                    break
                page += 1

            except ApiException as e:
                if(e.status):
                    raise HTTPException(status_code=e.status, detail=str(e))

    return all_users