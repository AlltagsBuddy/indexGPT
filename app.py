from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
CORS(app)


load_dotenv()  # Lädt .env-Inhalte lokal, auf Render optional

app = Flask(__name__, template_folder="templates")

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

# Bisheriger Prompt-Endpunkt (kann beibehalten oder entfernt werden)
@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json()
    user_prompt = data.get("prompt", "")
    if not user_prompt:
        return jsonify({"error": "Kein Prompt übergeben."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.5-turbo",  # Neu: aktuelles Modell statt gpt-3.5
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7,
        )
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Neuer Chat-Endpunkt, der den gesamten Verlauf verarbeitet
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    if not messages:
        return jsonify({"error": "Keine Nachrichten übergeben."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.5-turbo",  # oder "gpt-4o" bzw. zukünftige Modelle
            messages=messages,
            temperature=0.7,
        )
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
