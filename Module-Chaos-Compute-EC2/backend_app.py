from flask import Flask, jsonify
import time, os

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "backend-ok"}), 200

@app.route("/process")
def process():
    time.sleep(0.5)
    return jsonify({"result": "order processed successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
