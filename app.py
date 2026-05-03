from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "sahiltoken123"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
MAKE_WEBHOOK_URL = os.environ.get("MAKE_WEBHOOK_URL")

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    requests.post(MAKE_WEBHOOK_URL, json=data)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)