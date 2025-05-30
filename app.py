from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Carregar variáveis de ambiente (funciona localmente com .env)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Inicializar Firebase Admin com a chave vinda da variável de ambiente
firebase_key_json = os.environ.get("FIREBASE_KEY")
if not firebase_key_json:
    raise ValueError("FIREBASE_KEY environment variable not set")

# Parsear a string JSON da chave
firebase_key = json.loads(firebase_key_json)
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)

# Iniciar o banco
db = firestore.client()

# Carregar modelo BERT do Hugging Face
MODEL_PATH = "xavierruth/spotify-pnl"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

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

        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            rating = torch.argmax(probs, dim=1).item() + 1

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
