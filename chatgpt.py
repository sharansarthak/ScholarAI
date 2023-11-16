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

def chatgpt(question, answer):


    conversations = [{"role": "system", "content": "You are a helpful assistant who specilaizes in enhancing users scholarship essays"}]

    request_message = "The question asked in my scholarship application is this: "+str(question)+" My Reponse is: "+str(answer)+" Provide improved essay keeping similar word count"
    request_message_formatted = {'content': request_message, 'role': 'user'}

    conversations.append(request_message_formatted)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversations
    )

    print(response.choices[0].message.content)

def get_interview_feedback_chatgpt(question, response):


    conversations = [{"role": "system", "content": "You are a helpful interview preparation assistant who will provide feedback for improvement when provided with the questions and user's transcribe audio for their response"}]

    request_message = "The question asked in the interview is this: "+str(question)+" The transcribed response is: "+str(answer)+" Provide feedback to imrpove my response to ace the interview."
    request_message_formatted = {'content': request_message, 'role': 'user'}

    conversations.append(request_message_formatted)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversations
    )

    print(response.choices[0].message.content)

#write_chat('zeeshan', {'message':  {"role": "user", "content": "Who won the world series in 2020?"}})
#print(read_chat('zeeshan')[0])
message="Name 2 hard to aattain scholarships?"

question = "Describe a challenging situation you faced in your academic journey and how you overcame it. How did this experience shape your character and contribute to your personal growth?"
answer = "During my sophomore year, I encountered a challenging academic setback when I struggled with advanced calculus. Determined to overcome this obstacle, I sought additional tutoring, formed study groups, and dedicated extra hours to grasp the concepts. This perseverance not only improved my grades but also honed my problem-solving skills. The experience taught me resilience, emphasizing the importance of seeking support when faced with challenges. Overcoming this academic hurdle has positively shaped my character, instilling a proactive approach to difficulties. It has contributed significantly to my personal growth by fostering resilience, adaptability, and a passion for continuous learning."
chatgpt('zeeshan', message)
#print(response.choices[0].message.content)
