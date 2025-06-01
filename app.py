from flask import Flask, render_template, request, jsonify
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

HF_API_URL = "https://api-inference.huggingface.co/models/xavierruth/spotify-pnl"
HF_API_TOKEN = os.environ.get("HF_API_KEY")

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def hf_predict(text):
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # levanta erro se a requisição falhar
    return response.json()

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

        result = classifier(text)
        label = result[0]["label"]
        rating = int(label.replace("LABEL_", "")) + 1

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
