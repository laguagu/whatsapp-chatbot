import json
import logging
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
# Import the OpenAI class
from openai import OpenAI

# Ladataan ympäristömuuttujat .env-tiedostosta
load_dotenv()

# Alustetaan API-avaimet ja URL:t
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Instantiate the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Alustetaan Flask-sovellus
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# AI-vastauksen generointi OpenAI:n avulla
def generate_ai_response(message_text):
    try:
        # Use the new client method
        response = client.chat.completions.create(
            model="gpt-4.1-mini-2025-04-14",
            messages=[
                {"role": "system", "content": "Olet avulias WhatsApp-assistentti, joka vastaa lyhyesti ja ytimekkäästi."},
                {"role": "user", "content": message_text}
            ],
            max_tokens=300,
        )
        logging.info(f"AI-vastaus: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Virhe AI-vastauksessa: {e}")
        return "Pahoittelut, en pystynyt käsittelemään viestiäsi juuri nyt."

# WhatsApp-viestin lähettäminen
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
        logging.info(f"Viesti lähetetty onnistuneesti: {response.json()}")
        return True
    else:
        logging.error(f"Virhe viestin lähetyksessä: {response.text}")
        return False

# Testiviesti selaimesta (GET-pyyntö)
@app.route('/testmessage', methods=['GET'])
def test_send_message():
    recipient = request.args.get('to', '')
    message = request.args.get('message', 'Tämä on testiviestiä WhatsApp API -botilta!')
    
    if not recipient:
        return jsonify({
            "error": "Puhelinnumero puuttuu! Käytä parametria 'to', esim: /testmessage?to=358401234567"
        }), 400
    
    # Yritetään lähettää viesti
    result = send_whatsapp_message(recipient, message)
    
    return jsonify({
        "success": result,
        "to": recipient,
        "message": message
    })

# AI-vastauksen lähetys (GET-pyyntö)
@app.route('/askAI', methods=['GET'])
def ask_ai():
    recipient = request.args.get('to', '')
    question = request.args.get('question', '')
    
    if not recipient:
        return jsonify({
            "error": "Puhelinnumero puuttuu! Käytä parametria 'to', esim: /askAI?to=358401234567&question=Mitä kuuluu?"
        }), 400
    
    if not question:
        return jsonify({
            "error": "Kysymys puuttuu! Käytä parametria 'question', esim: /askAI?to=358401234567&question=Mitä kuuluu?"
        }), 400
    
    # Generoidaan AI-vastaus
    ai_response = generate_ai_response(question)
    
    # Lähetetään vastaus
    result = send_whatsapp_message(recipient, ai_response)
    
    return jsonify({
        "success": result,
        "to": recipient,
        "question": question,
        "ai_response": ai_response
    })

# Reitti viestien lähettämiseen (POST-pyyntö)
@app.route('/send_message', methods=['POST'])
def send_message_route():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        if not phone_number or not message:
            return jsonify({"status": "error", "message": "Puhelinnumero ja viesti vaaditaan"}), 400
        
        # Varmista että numero on oikeassa muodossa
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
            
        # Lähetä viesti
        result = send_whatsapp_message(phone_number, message)
        
        if result:
            return jsonify({"status": "success", "message": "Viesti lähetetty onnistuneesti"}), 200
        else:
            return jsonify({"status": "error", "message": "Viestin lähetys epäonnistui"}), 500
    
    except Exception as e:
        logging.error(f"Virhe viestin lähettämisessä: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Reitti AI-viestin lähettämiseen (POST-pyyntö)
@app.route('/send_ai_message', methods=['POST'])
def send_ai_message_route():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        question = data.get('question')
        
        if not phone_number or not question:
            return jsonify({"status": "error", "message": "Puhelinnumero ja kysymys vaaditaan"}), 400
        
        # Varmista että numero on oikeassa muodossa
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        # Generoi AI-vastaus
        ai_response = generate_ai_response(question)
        
        # Lähetä viesti
        result = send_whatsapp_message(phone_number, ai_response)
        
        if result:
            return jsonify({
                "status": "success", 
                "message": "AI-vastaus lähetetty onnistuneesti",
                "ai_response": ai_response
            }), 200
        else:
            return jsonify({"status": "error", "message": "Viestin lähetys epäonnistui"}), 500
    
    except Exception as e:
        logging.error(f"Virhe AI-viestin lähettämisessä: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Reitti template-viestien lähettämiseen
@app.route('/send_template', methods=['POST'])
def send_template_route():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        template_name = data.get('template_name')
        language_code = data.get('language_code', 'en_US')
        
        if not phone_number or not template_name:
            return jsonify({"status": "error", "message": "Puhelinnumero ja templaten nimi vaaditaan"}), 400
        
        # Varmista että numero on oikeassa muodossa
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
        logging.error(f"Virhe template-viestin lähettämisessä: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Etusivu
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
                <p>Käytettävissä olevat API-reitit:</p>
                
                <div class="endpoint">
                    <h3><span class="method">GET</span> /testmessage</h3>
                    <p>Lähetä testiviestiä selaimessa:</p>
                    <p><code>/testmessage?to=358401234567&message=Testi viesti</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">GET</span> /askAI</h3>
                    <p>Kysy AI:lta ja lähetä vastaus WhatsAppiin:</p>
                    <p><code>/askAI?to=358401234567&question=Mitä kuuluu?</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">POST</span> /send_message</h3>
                    <p>Lähetä viesti (JSON):</p>
                    <p><code>{"phone_number": "358401234567", "message": "Tervehdys!"}</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">POST</span> /send_ai_message</h3>
                    <p>Lähetä AI-vastaus (JSON):</p>
                    <p><code>{"phone_number": "358401234567", "question": "Kuka on Suomen presidentti?"}</code></p>
                </div>
                
                <div class="endpoint">
                    <h3><span class="method">POST</span> /send_template</h3>
                    <p>Lähetä template-viesti (JSON):</p>
                    <p><code>{"phone_number": "358401234567", "template_name": "hello_world", "language_code": "en_US"}</code></p>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)