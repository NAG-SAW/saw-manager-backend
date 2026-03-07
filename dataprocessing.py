from dataclasses import dataclass

import pandas as pd


@dataclass
class User:
    User_ID: int
    Name: str
    Passwort_Authentik: str
    Passwort_WiFi: str
    Email: str
    Rolle: str
    Gruppe: str
    Geräte: str
    RFID_Chip: str

## Später mit DB oder Authentik requests ersetzen
def getAllUsers() -> list[User]:
    df = pd.read_csv('fakeusers.csv', delimiter=',')
    return [User(**row) for row in df.to_dict(orient='records')]

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




