
import requests


def send_test_message():
    url = "http://localhost:5000/send_message"
    
    payload = {
        "phone_number": "35850500505050",  # Vastaanottajan numero
        "message": "Moi mitä kuuluu?"  # Lähetettävä viesti
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Vastaus: {response.text}")

def send_ai_message():
    url = "http://localhost:5000/send_ai_message"
    
    payload = {
        "phone_number": "35850500505050",  # Vastaanottajan numero
        "question": "Mitä olet mieltä tekoälystä?"  # Kysymys AI:lle
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Vastaus: {response.text}")

def send_template():
    url = "http://localhost:5000/send_template"
    
    payload = {
        "phone_number": "35850500505050",  # Vastaanottajan numero
        "template_name": "hello_world",
        "language_code": "en_US"
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Vastaus: {response.text}")

if __name__ == "__main__":
    print("WhatsApp API Testi")
    print("------------------")
    print("1. Lähetä tavallinen viesti")
    print("2. Lähetä AI-vastaus")
    print("3. Lähetä template-viesti")
    
    choice = input("Valitse toiminto (1-3): ")
    
    if choice == "1":
        send_test_message()
    elif choice == "2":
        send_ai_message()
    elif choice == "3":
        send_template()
    else:
        print("Virheellinen valinta")