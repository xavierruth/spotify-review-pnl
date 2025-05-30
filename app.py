from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Firebase Admin com chave do ambiente
firebase_key_json = os.environ.get("FIREBASE_KEY")
if not firebase_key_json:
    raise ValueError("FIREBASE_KEY environment variable not set")

firebase_key = json.loads(firebase_key_json)
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)

# Iniciar o banco
db = firestore.client()

# Configuração do Hugging Face
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")  # Deve estar no .env
MODEL_ID = "xavierruth/spotify-pnl"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

# Iniciar Flask
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

        # Enviar para Hugging Face API
        response = requests.post(HF_API_URL, headers=headers, json={"inputs": text})
        response.raise_for_status()

        outputs = response.json()
        # Espera-se que seja uma lista com dicionários [{"label": "LABEL_2", "score": 0.85}, ...]
        predicted = max(outputs, key=lambda x: x['score'])
        label = predicted["label"]
        rating = int(label.replace("LABEL_", "")) + 1  # LABEL_0 → 1, LABEL_4 → 5

        # Salvar no Firestore
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
