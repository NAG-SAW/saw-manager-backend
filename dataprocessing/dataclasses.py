from dataclasses import dataclass


#TODO: Update
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