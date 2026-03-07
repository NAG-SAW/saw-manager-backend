# Backend für den SAW Manager

Das Backend soll hauptsächlich die User-Daten an unser frontend geben damit wir sie anzeigen können.
Eventuell wirds auch nützlich sein für andere frontend Bereiche wie E-Wash aber mal schauen.

Wir brauchen wahrscheinlich auch eine Datenbank für die Kontodaten, da wir diese nur unschön mit Authentik speichern können.

## Anforderungen:

- [ ] Schnittstelle für requesten von Userdaten
  - [ ] Benutzername
  - [ ] Vor- und Nachname
  - [ ] E-Mail Adresse
  - [ ] Kontodaten
  - [ ] Sportchip
  - [ ] Evtl. Netzwerk Infos (generierte passwörter für SAW Legacy)
- [ ] Schnitstellen für das updaten von Daten
  - [ ] Kontodaten
  - [ ] Sportchip
  - [ ] Evtl. Netzwerk Infos (falls wir das nicht immer auf unify und hier machen möchten)
  - [ ] WiFi passtwort anpassen?
- [ ] Authentik permission checks (Authlib soll wohl ganz gut sein)


## Was wir benutzen für die API

* Python
* FastAPI[https://github.com/fastapi/fastapi]
* Authlib[https://docs.authlib.org/en/latest/client/fastapi.html]
