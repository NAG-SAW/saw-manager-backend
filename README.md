# Backend für den SAW Manager

Das Backend soll hauptsächlich die User-Daten an unser frontend geben damit wir sie anzeigen können.
Eventuell wirds auch nützlich sein für andere frontend Bereiche wie E-Wash aber mal schauen.

Wir brauchen wahrscheinlich auch eine Datenbank für die Kontodaten, da wir diese nur unschön mit Authentik speichern können.

## Anforderungen:

- [X] Schnittstelle für requesten von Userdaten
  - [X] Filtern nach bestimmten attributes
- [] Schnittstelle für requesten von Userdaten für spezifischen User
- [ ] Schnitstellen für das updaten von Daten
- [x] Authentik permission checks (Authlib soll wohl ganz gut sein)


## Was wir benutzen für die API

* Python
* FastAPI[https://github.com/fastapi/fastapi]
* Authlib[https://docs.authlib.org/en/latest/client/fastapi.html]
* itsdangerous ist auch in den requirements, weil es von SessionMiddleware (included in Authlib glaube ich) benutzt wird für signing und verification [https://pypi.org/project/itsdangerous/]
