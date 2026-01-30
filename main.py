from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json

    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400

    payload = {
        "message": data["message"]
    }

    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(response.json())
