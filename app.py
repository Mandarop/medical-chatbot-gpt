# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file (only used locally)
load_dotenv()

# Get the API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Allow all origins (good for mobile apps)

# Simple language detection for Hindi/Marathi
def is_hindi_or_marathi(text):
    hindi_marathi_pattern = re.compile(r'[\u0900-\u097F]')  # Unicode range for Devanagari (Hindi/Marathi)
    return bool(hindi_marathi_pattern.search(text))

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Adjust system prompt to focus on mental health
        system_message = "You are a helpful and empathetic mental health assistant. Please only talk about mental health topics."

        # Detect language and adjust response accordingly
        if is_hindi_or_marathi(user_message):
            # Change response tone if Hindi/Marathi
            system_message += " Respond empathetically in Hindi or Marathi, but in English text."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
