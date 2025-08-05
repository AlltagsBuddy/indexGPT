from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Flask-App initialisieren und CORS aktivieren
app = Flask(__name__, template_folder="templates", static_folder="")
CORS(app)

# OpenAI-Client nach neuem API-Schema initialisieren
openai_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.route("/")
def index():
    # index.html aus dem Wurzelverzeichnis ausliefern
    return send_from_directory(".", "index.html")

@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json(silent=True) or {}
    user_prompt = data.get("prompt", "").strip()
    if not user_prompt:
        return jsonify({"error": "Kein Prompt übergeben."}), 400
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",  # oder gpt-3.5-turbo, wenn nötig
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        # Fehler ausgeben (erscheint in Render-Logs) und an Frontend weitergeben
        print(f"Fehler im Prompt-Endpunkt: {e}")
        return jsonify({"response": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Keine Nachrichten übergeben."}), 400
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        print(f"Fehler im Chat-Endpunkt: {e}")
        return jsonify({"response": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
