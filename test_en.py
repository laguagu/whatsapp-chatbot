import requests


def send_test_message():
    url = "http://localhost:5000/send_message"
    
    payload = {
        "phone_number": "35850500505050",  # Recipient's number
        "message": "Hello, how are you?"  # Message to send
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def send_ai_message():
    url = "http://localhost:5000/send_ai_message"
    
    payload = {
        "phone_number": "35850500505050",  # Recipient's number
        "question": "What do you think about artificial intelligence?"  # Question for AI
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def send_template():
    url = "http://localhost:5000/send_template"
    
    payload = {
        "phone_number": "35850500505050",  # Recipient's number
        "template_name": "hello_world",
        "language_code": "en_US"
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    print("WhatsApp API Test")
    print("------------------")
    print("1. Send a regular message")
    print("2. Send an AI response")
    print("3. Send a template message")
    
    choice = input("Select an action (1-3): ")
    
    if choice == "1":
        send_test_message()
    elif choice == "2":
        send_ai_message()
    elif choice == "3":
        send_template()
    else:
        print("Invalid selection")