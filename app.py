"""
Flask‑Anwendung für die AlltagsBuddy ChatGPT‑Integration.

Dieses Skript definiert zwei API‑Endpunkte:
1. `/api/prompt` – nimmt einen einzelnen Prompt entgegen und gibt eine Antwort zurück.
2. `/api/chat`   – akzeptiert ein Nachrichten‑Array mit Verlauf für fortlaufende Chats.

Die Reihenfolge der Initialisierung wurde korrigiert: Erst wird die Flask‑App erstellt,
dann CORS aktiviert. Anschließend wird der OpenAI‑API‑Key geladen.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Lokale Umgebungsvariablen laden (auf Render optional, da Variablen dort über das Dashboard gesetzt werden)
load_dotenv()

# Flask‑App initialisieren und CORS aktivieren
app = Flask(__name__, template_folder="templates")
CORS(app)

# OpenAI‑API‑Schlüssel aus der Umgebung lesen
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index() -> str:
    """Liefert die Startseite der Anwendung."""
    return render_template("index.html")

@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    """
    Verarbeitet einen einzelnen Prompt von der Frontend‑Seite.
    Erwartet JSON im Format {"prompt": "..."} und gibt die Antwort der OpenAI‑API zurück.
    """
    data = request.get_json(silent=True) or {}
    user_prompt = data.get("prompt", "").strip()
    if not user_prompt:
        return jsonify({"error": "Kein Prompt übergeben."}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.5-turbo",  # aktuelles Modell
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
        )
        answer = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Verarbeitet einen Chat mit Verlauf. Erwartet JSON mit einem
    Array "messages", z.B. {"messages": [{"role": "user", "content": "..."}, ...]}.
    Gibt die Antwort der OpenAI‑API zurück.
    """
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    # Validierung: Es muss mindestens eine Nachricht vorhanden sein
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Keine Nachrichten übergeben."}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # oder "gpt-4o" bzw. zukünftige Modelle
            messages=messages,
            temperature=0.7,
        )
        answer = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Lokale Entwicklungsumgebung
    app.run(debug=True)
