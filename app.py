from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import os

# Flask App initialisieren
app = Flask(__name__, template_folder="templates")
CORS(app)

# OpenAI-Client initialisieren mit Render-Umgebungsvariable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("../index.html")  # Oder nur "index.html", wenn du die Datei verschiebst

@app.route("/chat")
def chat_ui():
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Keine Nachrichten übergeben."}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # oder gpt-4/gpt-4o
            messages=messages,
            temperature=0.7
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
