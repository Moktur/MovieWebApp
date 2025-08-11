# MovieApp

Eine einfache Flask-Webapp zur Verwaltung persönlicher Lieblingsfilme pro User, mit Daten von der OMDb API.

---

## Features

- Benutzer anlegen und auflisten (Achtung: Es ist nur ein Benutzername mit demselben Namen möglich!)
- Lieblingsfilme hinzufügen, bearbeiten und löschen
- Filmdaten (Titel, Regisseur, Jahr, Poster) werden von OMDb API geladen
- SQLite Datenbank mit SQLAlchemy ORM

---

## Voraussetzungen

- Python 3.8 oder höher
- Virtuelle Umgebung empfohlen

---

## Installation & Setup

1. Repository klonen:
    ```bash
    git clone https://github.com/dein-benutzername/movieapp.git
    cd movieapp
    ```

2. Virtuelle Umgebung anlegen und aktivieren:
    ```bash
    python -m venv venv
    source venv/bin/activate      # Linux/macOS
    venv\Scripts\activate.bat     # Windows
    ```

3. Abhängigkeiten installieren:
    ```bash
    pip install -r requirements.txt
    ```

4. Umgebungsvariable für OMDb API-Key setzen:

    Erstelle eine `.env` Datei im Projektverzeichnis mit folgendem Inhalt:
    ```
    API_KEY=dein_omdb_api_key
    ```

    Falls noch kein API-Key vorhanden, hier anfordern: [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)

5. Datenbank initialisieren:

    Die SQLite-Datenbank wird automatisch beim ersten Start erstellt.

6. Server starten:
    ```bash
    python app.py
    ```

7. Im Browser öffnen:
    ```
    http://localhost:5002/
    ```

---

## Nutzung

- Auf der Startseite Benutzer anlegen oder auswählen
- Für jeden Benutzer Lieblingsfilme hinzufügen, bearbeiten oder löschen

---

## Probleme & Fragen

Bei Fehlern bitte prüfen, ob:

- Der API-Key korrekt gesetzt ist
- Die virtuelle Umgebung aktiv ist
- Alle Abhängigkeiten installiert sind


---

Viel Spaß mit der MovieApp! 🎬
