# WhatsApp AI Chatbot

A simple but powerful WhatsApp chatbot that integrates with OpenAI's GPT models to provide AI-powered responses via WhatsApp. Built with Flask and the WhatsApp Cloud API.

## Features

- 🤖 AI-powered responses using OpenAI's GPT models
- 📱 Direct WhatsApp messaging integration
- 📝 Support for text messages and template messages
- 🌐 Simple REST API for integration with other systems
- 🌍 Available in multiple languages (English and Finnish)

## Requirements

- Python 3.8 or higher
- WhatsApp Business Account and API access
- OpenAI API key
- uv package manager (recommended)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/laguagu/whatsapp-chatbot.git
cd whatsapp-chatbot
```

### 2. Install dependencies using uv

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

The project already includes a `pyproject.toml` file with the necessary dependencies.

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit the `.env` file and add your credentials:

```
WHATSAPP_API_TOKEN=your_whatsapp_api_token_here
WHATSAPP_PHONE_ID=your_whatsapp_phone_id_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Obtain WhatsApp API credentials

1. Create a Meta Developer and follow up instructions [developers.facebook.com](https://developers.facebook.com/docs/whatsapp/cloud-api/get-started)
2. Set up a WhatsApp Business account
3. Create an app and add the WhatsApp API product
4. Get your Phone Number ID and API Token from the app dashboard

## Usage

### Starting the server

```bash
# Start the Flask server
python main.py  # Finnish version
# OR
python main_en.py  # English version
```

The server will start on http://localhost:5000

### Sending messages

#### Using the test script

```bash
# Run the test script
python test.py  # Finnish version
# OR
python test_en.py  # English version
```

Follow the prompts to send different types of messages.

#### Using the web interface

Open your browser and navigate to:

- Send a test message: http://localhost:5000/testmessage?to=358XXXXXXXXX&message=Hello
- Ask AI a question: http://localhost:5000/askAI?to=358XXXXXXXXX&question=What%20is%20the%20capital%20of%20France?

#### Using API endpoints

The server provides these API endpoints:

| Endpoint           | Method | Description                   | Payload Example                                                                              |
| ------------------ | ------ | ----------------------------- | -------------------------------------------------------------------------------------------- |
| `/send_message`    | POST   | Send a regular text message   | `{"phone_number": "358XXXXXXXXX", "message": "Hello"}`                                       |
| `/send_ai_message` | POST   | Send an AI-generated response | `{"phone_number": "358XXXXXXXXX", "question": "What's the weather?"}`                        |
| `/send_template`   | POST   | Send a template message       | `{"phone_number": "358XXXXXXXXX", "template_name": "hello_world", "language_code": "en_US"}` |

## WhatsApp API Limitations

- **24-hour window**: Regular messages can only be sent within 24 hours after the user has sent a message to your business
- **Template messages**: Can be sent at any time but must be pre-approved
- **Test environment**: In development, you might need to add recipient phone numbers to your allowed test contacts

## Troubleshooting

### Common Errors

- **"Recipient phone number not in allowed list"**: Add the number to your allowed test contacts in the Meta Developer Portal or have the user message your business first
- **"Message sending failed"**: Check your WhatsApp API Token and Phone ID
- **"Error in AI response"**: Verify your OpenAI API key and check API usage limits

### Logs

The server logs all messages and errors. Check the console output for detailed logs when troubleshooting.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](LICENSE)
