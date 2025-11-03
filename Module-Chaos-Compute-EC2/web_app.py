from flask import Flask, jsonify, request
import os, requests

app = Flask(__name__)

TARGET_HOST = os.getenv("TARGET_HOST", "backend")
TARGET_PORT = os.getenv("TARGET_PORT", "5000")

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    try:
        res = requests.get(f"http://{TARGET_HOST}:{TARGET_PORT}/process")
        return jsonify({"checkout_status": "success", "backend_reply": res.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
