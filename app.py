from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "sahiltoken123"  # CHANGE THIS to what you set in Meta

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """WhatsApp verification endpoint"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode and token and mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return '', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Receive WhatsApp messages"""
    data = request.json
    print("Message received:", data)
    
    # Parse the message
    try:
        entry = data.get('entry', [])[0]
        changes = entry.get('changes', [])[0]
        value = changes.get('value', {})
        message = value.get('messages', [])[0]
        
        if message:
            from_number = message.get('from')
            text = message.get('text', {}).get('body', '')
            print(f"From: {from_number}, Message: {text}")
    except Exception as e:
        print(f"Error parsing: {e}")
    
    return jsonify({"status": "ok"}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)