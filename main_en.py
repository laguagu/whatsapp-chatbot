import json
import logging
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize API keys and URLs
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask application
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Generate AI response using OpenAI
def generate_ai_response(message_text):
    try:
        # Use the new client method
        response = client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a helpful WhatsApp assistant who responds briefly and concisely."},
                {"role": "user", "content": message_text}
            ],
            max_tokens=300,
        )
        logging.info(f"AI response: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in AI response: {e}")
        return "Sorry, I couldn't process your message right now."

# Send WhatsApp message
def send_whatsapp_message(phone_number, message):
    url = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        logging.info(f"Message sent successfully: {response.json()}")
        return True
    else:
        logging.error(f"Error sending message: {response.text}")
        return False

# Test message from browser (GET request)
@app.route('/testmessage', methods=['GET'])
def test_send_message():
    recipient = request.args.get('to', '')
    message = request.args.get('message', 'This is a test message from the WhatsApp API bot!')
    
    if not recipient:
        return jsonify({
            "error": "Phone number missing! Use the 'to' parameter, e.g.: /testmessage?to=358401234567"
        }), 400
    
    # Try to send the message
    result = send_whatsapp_message(recipient, message)
    
    return jsonify({
        "success": result,
        "to": recipient,
        "message": message
    })

# Send AI response (GET request)
@app.route('/askAI', methods=['GET'])
def ask_ai():
    recipient = request.args.get('to', '')
    question = request.args.get('question', '')
    
    if not recipient:
        return jsonify({
            "error": "Phone number missing! Use the 'to' parameter, e.g.: /askAI?to=358401234567&question=How are you?"
        }), 400
    
    if not question:
        return jsonify({
            "error": "Question missing! Use the 'question' parameter, e.g.: /askAI?to=358401234567&question=How are you?"
        }), 400
    
    # Generate AI response
    ai_response = generate_ai_response(question)
    
    # Send response
    result = send_whatsapp_message(recipient, ai_response)
    
    return jsonify({
        "success": result,
        "to": recipient,
        "question": question,
        "ai_response": ai_response
    })

# Route for sending messages (POST request)
@app.route('/send_message', methods=['POST'])
def send_message_route():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        if not phone_number or not message:
            return jsonify({"status": "error", "message": "Phone number and message are required"}), 400
        
        # Ensure the number is in the correct format
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
            
        # Send message
        result = send_whatsapp_message(phone_number, message)
        
        if result:
            return jsonify({"status": "success", "message": "Message sent successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Message sending failed"}), 500
    
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Route for sending AI messages (POST request)
@app.route('/send_ai_message', methods=['POST'])
def send_ai_message_route():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        question = data.get('question')
        
        if not phone_number or not question:
            return jsonify({"status": "error", "message": "Phone number and question are required"}), 400
        
        # Ensure the number is in the correct format
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        # Generate AI response
        ai_response = generate_ai_response(question)
        
        # Send message
        result = send_whatsapp_message(phone_number, ai_response)
        
        if result:
            return jsonify({
                "status": "success", 
                "message": "AI response sent successfully",
                "ai_response": ai_response
            }), 200
        else:
            return jsonify({"status": "error", "message": "Message sending failed"}), 500
    
    except Exception as e:
        logging.error(f"Error sending AI message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Route for sending template messages
@app.route('/send_template', methods=['POST'])
def send_template_route():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        template_name = data.get('template_name')
        language_code = data.get('language_code', 'en_US')
        
        if not phone_number or not template_name:
            return jsonify({"status": "error", "message": "Phone number and template name are required"}), 400
        
        # Ensure the number is in the correct format
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {WHATSAPP_API_TOKEN}"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return jsonify({"status": "success", "response": response.json()}), 200
        else:
            return jsonify({"status": "error", "message": response.text}), response.status_code
    
    except Exception as e:
        logging.error(f"Error sending template message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Home page
@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>WhatsApp API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
                .container { max-width: 800px; margin: 0 auto; }
                h1 { color: #4CAF50; }
                .endpoint { background: #f5f5f5; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
                .method { font-weight: bold; color: #2196F3; }
                code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>WhatsApp API</h1>
                <p>Available API endpoints:</p>
                
                <div class="endpoint">
                    <h3><span class="method">GET</span> /testmessage</h3>
                    <p>Send a test message via browser:</p>
                    <p><code>/testmessage?to=358401234567&message=Test message</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">GET</span> /askAI</h3>
                    <p>Ask AI and send response to WhatsApp:</p>
                    <p><code>/askAI?to=358401234567&question=How are you?</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">POST</span> /send_message</h3>
                    <p>Send message (JSON):</p>
                    <p><code>{"phone_number": "358401234567", "message": "Hello!"}</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">POST</span> /send_ai_message</h3>
                    <p>Send AI response (JSON):</p>
                    <p><code>{"phone_number": "358401234567", "question": "Who is the president of the United States?"}</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">POST</span> /send_template</h3>
                    <p>Send template message (JSON):</p>
                    <p><code>{"phone_number": "358401234567", "template_name": "hello_world", "language_code": "en_US"}</code></p>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)