from flask import Flask, request
import africastalking
from google import genai

# Gemini API
gemini_client = genai.Client(api_key="AIzaSyA4TctigTH81x4jagh_k1yOxiLiJuGSiCI")
chat = gemini_client.chats.create(model="gemini-2.5-flash")

# Africa's Talking credentials
username = "sandbox"
api_key = "atsk_45e7e1089c25a5f5d1b077778a34c92aeedf1dc3c477727fd8ecae7f7fb9d04fc66ca46b"

africastalking.initialize(username, api_key)
sms = africastalking.SMS

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_reply():
    message = request.form.get('text')
    phone = request.form.get('from')

    # Send message to Gemini
    response = chat.send_message(message)
    reply = response.text

    # Send SMS back
    sms.send(reply, [phone])

    return "OK"

if __name__ == '__main__':
    app.run(port=5000)