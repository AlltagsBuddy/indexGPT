from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Nur lokal nötig – auf Render kannst du das ignorieren, wenn du Umgebungsvariable manuell setzt
load_dotenv()

app = Flask(__name__, template_folder="templates")

# API-Key aus Umgebungsvariable holen
openai.api_key = os.getenv("OPENAI_API_KEY")


# Route für Startseite (HTML-Formular)
@app.route("/")
def index():
    return render_template("index.html")


# API-Route für Prompteingabe
@app.route("/api/prompt", methods=["POST"])
def handle_prompt():
    data = request.get_json()
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "Kein Prompt übergeben."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Lokaler Start (nicht notwendig bei Render)
if __name__ == "__main__":
    app.run(debug=True)
