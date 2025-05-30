from flask import Flask, render_template, request, jsonify
import os
import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Em ambiente local, carregue o .env
if os.environ.get("RAILWAY_ENVIRONMENT") is None:
    from dotenv import load_dotenv
    load_dotenv()

# Pegar chave do Firebase
firebase_key_json = os.environ.get("FIREBASE_KEY")
if not firebase_key_json:
    raise ValueError("FIREBASE_KEY environment variable not set")

# Convertendo a chave JSON em dicionário
firebase_key = json.loads(firebase_key_json)

# Inicializando o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Hugging Face
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
MODEL_ID = "xavierruth/spotify-pnl"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

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

        # Envio à API Hugging Face
        response = requests.post(HF_API_URL, headers=headers, json={"inputs": text})
        response.raise_for_status()
        outputs = response.json()
        print("API response:", outputs)
        
        predicted = max(outputs, key=lambda x: x['score'])
        label = predicted["label"]
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
    app.run(debug=True)
