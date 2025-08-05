from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Nur lokal nötig

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

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

if __name__ == "__main__":
    app.run(debug=True)
