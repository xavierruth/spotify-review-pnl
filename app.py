from flask import Flask, render_template, request, jsonify
from transformers import pipeline
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

# ⚡ Carrega o modelo Hugging Face apenas uma vez
print("Carregando modelo Hugging Face...")
classifier = pipeline("text-classification", model="xavierruth/spotify-pnl")
print("Modelo carregado com sucesso.")

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

        # ⚡ Usa o modelo já carregado
        result = classifier(text)
        label = result[0]["label"]
        rating = int(label.replace("LABEL_", "")) + 1

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
