from openai import OpenAI
import os
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("hhh2023-a2da1-firebase-adminsdk-h2zwt-5ae5f17a8b.json")
firebase_admin.initialize_app(cred)

db=firestore.client()


# Read the API key from a file
with open("APIKEY", "r") as file:
    api_key = file.read().strip()

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = api_key

client = OpenAI()



def write_chat(username, request):    
    for message in request:
        db.collection('users').document(username).collection('chat').add({'message':message})

def read_chat(username):
    docs = db.collection('users').document(username).collection('chat').get()
    result = []
    for doc in docs:
        result.append(doc.to_dict()['message'])
    return result

def chatgpt(username, request_message):

    request_message_formatted = {'content': request_message, 'role': 'user'}
    messages_to_send = read_chat(username) + [request_message_formatted]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send
    )

    response_message_formatted = {'content': response.choices[0].message.content, 'role': 'assistant'}
    messages = [request_message_formatted]+[response_message_formatted]

    write_chat(username, messages)

#write_chat('zeeshan', {'message':  {"role": "user", "content": "Who won the world series in 2020?"}})
#print(read_chat('zeeshan')[0])
message="Name 2 hard to aattain scholarships?"
chatgpt('zeeshan', message)
print(read_chat('zeeshan'))
#print(response.choices[0].message.content)
