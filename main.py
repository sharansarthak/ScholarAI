
import threading
# from moviepy.editor import VideoFileClip, AudioFileClip
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# from speechToText import transcribe_audio
# from recordAudio import record_audio
# from recordVideo import record_video   
from moviepy.editor import VideoFileClip, AudioFileClip
#from speechToText import extract_audio_from_video, transcribe_audio
from openai import OpenAI
import os
import firebase_admin
from firebase_admin import auth, credentials, firestore
from openai import OpenAI
from speechToText import extract_audio, transcribe_audio
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

cred = credentials.Certificate("hhh2023-a2da1-firebase-adminsdk-h2zwt-5ae5f17a8b.json")
firebase_admin.initialize_app(cred)

db=firestore.client()
# Read the API key from a file
with open("APIKEY", "r") as file:
    api_key = file.read().strip()

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = api_key

client = OpenAI()


@app.route('/upload_video', methods=['POST'])
def upload_video():
    video_file = request.files['video']
    if video_file:
        video_path = os.path.join('uploads', video_file.filename)
        video_file.save(video_path)
        
        # Process the video file and get feedback
        ai_feedback = process_video_and_get_feedback(video_path)

        # Return the AI feedback in the response
        return jsonify({"message": "Video uploaded successfully", "ai_feedback": ai_feedback})
    return jsonify({"error": "No video file provided"}), 400


def process_video_and_get_feedback(video_file_path):
    # Extract audio from the video
    audio_file_path =     extract_audio(video_path=video_file_path, audio_path="output_audio.wav")

    
    # Transcribe the audio to text
    transcribed_text = transcribe_audio("output_audio.wav")
    print(transcribed_text)
    # Prepare the conversation for AI feedback
    question = "Tell me about yourself"
    answer = transcribed_text
    conversations = [{"role": "system", "content": "You are an expert interview preparation assistant. Your goal is to provide constructive feedback and suggestions for improvement when given interview questions and a user's transcribed audio response. Emphasize clarity, relevance, and professionalism in your feedback."}]
    request_message = "The question asked in the interview is this: "+str(question)+" The transcribed response is: "+str(answer)+" Provide feedback to improve my response to ace the interview."
    request_message_formatted = {'content': request_message, 'role': 'user'}
    conversations.append(request_message_formatted)

    # Generate a response using OpenAI GPT-3.5-turbo
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversations
    )

    # Get the AI's response
    ai_response = response.choices[0].message.content
    testResponse = "Testing just random stuff"
    print(ai_response)
    return ai_response

def process_video(video_path):
    # Extract audio from video
    extract_audio(video_path=video_path, audio_path="output_audio.wav")
    text = transcribe_audio("output_audio.wav")
    

    # Transcribe audio
    # transcription = transcribe_audio(audio_path)  # Implement this function based on your transcription logic
    
    # Additional processing...

# Endpoint for user registration (sign-up)
@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get user data from the request
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Create a new user account with the provided email and password
        user = auth.create_user(
            email=email,
            password=password
        )

        return jsonify({'success': True, 'uid': user.uid}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get user data from the request
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Sign in the user with the provided email and password
        user = auth.get_user_by_email(email)
        user_token = auth.create_custom_token(user.uid)

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/request_chatgpt', methods=['POST'])
def chatgpt():

    request_message_formatted = {'content': request_message, 'role': 'user'}
    messages_to_send = read_chat(username) + [request_message_formatted]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_to_send
    )

    response_message_formatted = {'content': response.choices[0].message.content, 'role': 'assistant'}
    messages = [request_message_formatted]+[response_message_formatted]

    write_chat(username, messages)


@app.route('/write_chat', methods=['POST'])
def write_chat():
    # Get JSON data from the request
    data = request.json
    
    # Extract username and messages from the JSON data
    username = data.get('username')
    messages = data.get('messages', [])

    # Validate that both username and messages are present
    if not username or not messages:
        return jsonify({'error': 'Invalid request. Missing username or messages.'}), 400

    # Add messages to the chat in the database
    for message in messages:
        db.collection('users').document(username).collection('chat').add({'message': message})

    return jsonify({'success': True})

@app.route('/read_chat', methods=['GET'])
def read_chat():
    # Get username from the query parameters
    username = request.args.get('username')

    # Validate that username is present
    if not username:
        return jsonify({'error': 'Invalid request. Missing username.'}), 400

    # Retrieve messages from the chat in the database
    docs = db.collection('users').document(username).collection('chat').get()
    result = [doc.to_dict()['message'] for doc in docs]

    return jsonify(result)

@app.route('/add_scholarships', methods=['POST'])
def add_scholarships():
    data = request.json
    
    # Extract username and scholarships from the JSON data
    username = data.get('username')
    scholarships = data.get('scholarships', [])

    # Validate that both username and scholarships are present
    if not username or not scholarships:
        return jsonify({'error': 'Invalid request. Missing username or scholarships.'}), 400

    # Add scholarships to the database
    for scholarship in scholarships:
        title = scholarship.get('Title')
        if title:
            db.collection('users').document(username).collection('scholarship').document(title).set(scholarship)
        else:
            return jsonify({'error': 'Invalid scholarship. Missing title.'}), 400

    return jsonify({'success': True})


@app.route('/get_all_scholarships_brief', methods=['GET'])
def get_all_scholarships_brief():
    username = request.args.get('username')

    # Validate that username is present
    if not username:
        return jsonify({'error': 'Invalid request. Missing username.'}), 400

    docs = db.collection('users').document(username).collection('scholarship').get()
    result = []
    for doc in docs:
        scholarship_data = doc.to_dict()
        # Remove "Questions" and "Answers" fields if they exist
        scholarship_data.pop('Questions', None)
        scholarship_data.pop('Answers', None)
        scholarship_data.pop('Description', None)
        result.append(scholarship_data)

    return jsonify(result)


@app.route('/get_all_scholarships', methods=['GET'])
def get_all_scholarships():
    username = request.args.get('username')

    # Validate that username is present
    if not username:
        return jsonify({'error': 'Invalid request. Missing username.'}), 400

    docs = db.collection('users').document(username).collection('scholarship').get()
    result = [doc.to_dict() for doc in docs]

    return jsonify(result)

@app.route('/update_scholarship_answer', methods=['POST'])
def update_scholarship_answer():
    try:
        # Get data from the request
        data = request.json
        username = data.get('username')
        scholarship_title = data.get('title')
        index = data.get('index')
        updated_answer = data.get('updated_answer')

        print(data)

        # Validate required fields
        if not username or not scholarship_title or index is None or updated_answer is None:
            return jsonify({'error': 'Invalid request. Missing required fields.'}), 400

        # Retrieve the scholarship document
        scholarship_ref = db.collection('users').document(username).collection('scholarship').document(scholarship_title)
        scholarship_doc = scholarship_ref.get().to_dict()
        print(scholarship_doc)
        # Check if the scholarship exists
        if not scholarship_doc.exists:
            return jsonify({'error': 'Scholarship not found.'}), 404

        # Update the 'Answers' field at the specified index
        current_answers = scholarship_doc.get('Answers')

        if 0 <= index < len(current_answers):
            print(index)
            current_answers[index] = updated_answer
            scholarship_ref.update({'Answers': current_answers})
            return jsonify({'success': True})

        return jsonify({'error': 'Invalid index.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_all_resources', methods=['GET'])
def get_all_resources():
    try:
        username = request.args.get('username')
        docs = db.collection('users').document(username).collection('resource').get()
        result = []

        for doc in docs:
            resource_data = doc.to_dict()
            resource_data['category'] = doc.id  # Add the 'category' field
            result.append(resource_data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/submit_application', methods=['POST'])
def submit_application():
    try:
        data = request.json
        username = data.get('username')
        title = data.get('title')

        # Update the 'Submitted' field to True
        db.collection('users').document(username).collection('scholarship').document(title).update({'Submitted': True})

        return jsonify({'success': True, 'message': 'Application submitted successfully.'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_enhanced_essay', methods=['POST'])
def get_enhanced_essay():
    try:
        # Get question and answer from the request JSON
        question = request.json.get('question')
        answer = request.json.get('answer')

        # Define the initial conversation
        conversations = [{"role": "system", "content": "You are a helpful assistant who specializes in enhancing users' scholarship essays"}]

        # Format user's request message
        request_message = f"The question asked in my scholarship application is this: {question} My Response is: {answer} Provide just the improved essay keeping a similar word count (without title or unnecessary info)"
        request_message_formatted = {'content': request_message, 'role': 'user'}

        # Add user's request to the conversation
        conversations.append(request_message_formatted)

        # Generate a response using OpenAI GPT-3.5-turbo
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversations
        )

        # Get the AI's response from the choices
        ai_response = response.choices[0].message.content

        return jsonify({'success': True, 'response': ai_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_interview_feedback', methods=['POST'])
def get_interview_feedback():
    try:
        # Get question and answer from the request JSON
        question = request.json.get('question')
        answer = request.json.get('answer')

        conversations =[{"role": "system", "content": "You are an expert interview preparation assistant. Your goal is to provide constructive feedback and suggestions for improvement when given interview questions and a user's transcribed audio response. Emphasize clarity, relevance, and professionalism in your feedback."}] 

        request_message = "The question asked in the interview is this: "+str(question)+" The transcribed response is: "+str(answer)+" Provide feedback to imrpove my response to ace the interview."
        request_message_formatted = {'content': request_message, 'role': 'user'}

        conversations.append(request_message_formatted)

        # Generate a response using OpenAI GPT-3.5-turbo
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversations
        )

        # Get the AI's response from the choices
        ai_response = response.choices[0].message.content

        return jsonify({'success': True, 'response': ai_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_user_profile', methods=['POST'])
def update_user_profile():
    try:
        # Get data from the request
        data = request.json
        username = data.get('username')
        user_response = data.get('user_response')

        # Update user profile in the database
        db.collection('users').document(username).set(user_response)

        return jsonify({'success': True, 'message': 'User profile updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)