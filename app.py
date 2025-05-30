from flask import Flask, render_template, request, jsonify
import requests
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Carregamento do .env em ambiente local
if os.environ.get("RAILWAY_ENVIRONMENT") is None:
    from dotenv import load_dotenv
    load_dotenv()

# Inicialização do Firebase
firebase_key_json = os.environ.get("FIREBASE_KEY")
if not firebase_key_json:
    raise ValueError("FIREBASE_KEY environment variable not set")

firebase_key = json.loads(firebase_key_json)

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Hugging Face Inference API
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/xavierruth/spotify-pnl"
HUGGINGFACE_API_KEY = os.environ.get("HF_API_KEY")

# ✅ Função corrigida
def classify_text(text):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text}

    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        print("API response:", result)  # DEBUG

        # Lida com diferentes formatos de resposta
        if isinstance(result, list) and isinstance(result[0], dict):
            label = result[0]["label"]
        elif isinstance(result[0], list) and isinstance(result[0][0], dict):
            label = result[0][0]["label"]
        else:
            print("Formato inesperado:", result)
            return None

        return int(label.replace("LABEL_", "")) + 1
    except Exception as e:
        print("Hugging Face API error:", e)
        return None

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Empty review"}), 400

        rating = classify_text(text)
        if rating is None:
            return jsonify({"error": "Model inference failed"}), 500

        # Salva no Firebase
        db.collection("reviews").add({
            "text": text,
            "rating": rating
        })

        return jsonify({"rating": rating})

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run()
