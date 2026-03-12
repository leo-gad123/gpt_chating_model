from google import genai

client = genai.Client(api_key="AIzaSyA4TctigTH81x4jagh_k1yOxiLiJuGSiCI")
chat = client.chats.create(model="gemini-2.5-flash")  

while True:
     a=input("Enter your message: ")
     response1 = chat.send_message(a)
     print(response1.text)

