"""
Flask‑Anwendung für die AlltagsBuddy ChatGPT‑Integration.

Dieses Skript definiert zwei API‑Endpunkte:
1. `/api/prompt` – nimmt einen einzelnen Prompt entgegen und gibt eine Antwort zurück.
2. `/api/chat`   – akzeptiert ein Nachrichten‑Array mit Verlauf für fortlaufende Chats.

Die Reihenfolge der Initialisierung wurde korrigiert: Erst wird die Flask‑App erstellt,
dann CORS aktiviert. Anschließend wird der OpenAI‑API‑Key geladen.
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Umgebungsvariablen laden
load_dotenv()

# Flask initialisieren (Templates im Unterordner 'templates', statische Dateien im Wurzelverzeichnis)
app = Flask(__name__, template_folder="templates", static_folder="")

# CORS aktivieren
CORS(app)

# API‑Key setzen
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index() -> str:
    """Liefert die Startseite aus dem Wurzelverzeichnis."""
    return send_from_directory('.', 'index.html')

# Optional: wenn Sie chat.html über Flask ausliefern wollen
@app.route("/chat.html")
def chat_page():
    """Liefert die Chat‑Seite aus dem templates‑Verzeichnis."""
    return send_from_directory('templates', 'chat.html')

@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    """Verarbeitet einen einzelnen Prompt und gibt die Antwort der OpenAI‑API zurück."""
    data = request.get_json(silent=True) or {}
    user_prompt = data.get("prompt", "").strip()
    if not user_prompt:
        return jsonify({"error": "Kein Prompt übergeben."}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # nutzen Sie ein Modell, zu dem Sie Zugang haben
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
        )
        answer = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    """Verarbeitet einen Chatverlauf und gibt die Antwort der OpenAI‑API zurück."""
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Keine Nachrichten übergeben."}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
        answer = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
