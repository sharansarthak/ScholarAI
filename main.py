
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
    question = "Tell Us About The Biggest Challenge Youve Ever Faced"
    answer = transcribed_text
    conversations = [
        {
            "role": "system",
            "content": (
                "You are an expert interview preparation assistant. Your goal is to provide "
                "constructive feedback and suggestions for improvement when given interview "
                "questions and a user's transcribed audio response. Emphasize clarity, relevance, "
                "and professionalism in your feedback. Please format the feedback for HTML display. "
                "Use <p> for paragraphs, <br> for new lines, <ul> or <ol> for lists, and <strong> for "
                "emphasis. Ensure the feedback is well-structured and easy to read in an HTML document."
            )
        }
    ]
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

@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get user data from the request
        data = request.json
        email = data.get('email')
        password = data.get('password')
        phone_number = data.get('phone_number')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        # Create a new user account with the provided email and password
        user = auth.create_user(
            email=email,
            password=password
        )

        data_to_store = {
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "username": username,
            "first_name": first_name,
            "last_name": last_name
        }

        # Update user profile in the database
        db.collection('users').document(username).collection('personal_info').document('my_info').set(data_to_store)

        return jsonify({'success': True}), 201  # Corrected closing parenthesis

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

        return jsonify({'success': True, 'uid': user.uid, 'token': user_token}), 200

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

@app.route('/get_institution_scholarships', methods=['GET'])
def get_institution_scholarships():
    # username = request.args.get('username')

    result = [{
        "Scholarship Amount": "$10,000",
        "Deadline": "January 15, 2024",
        "Number of Recipients": 10,
        "Estimated Completion Time": "30 minutes",
        "Title": "CONTINUING UNDERGRADUATE AWARDS",
        "Requirements": ["STEM", "Innovation", "Academic Excellence"],
        "Description": "This scholarship is for students with a passion for STEM, a history of innovation, and demonstrated academic excellence.",
        "Questions": [
            "Describe your leadership activities (Minimum 3)",
            "How have you given back to your community?",
            "How have you demonstrated entrepreneurial skills?"
        ],
        "Answers": [
            "Leadership is a cornerstone of my academic and extracurricular pursuits. As the president of the student council, I orchestrated initiatives that fostered collaboration, inclusivity, and innovation within the student body. Leading a team of dedicated individuals, I organized events that not only enhanced the campus experience but also addressed pressing issues. Through my role, I developed strategic plans, delegated responsibilities, and implemented effective communication channels, cultivating a vibrant and engaged community.",
            "Giving back to my community is integral to my values. I initiated and led a local environmental cleanup campaign, mobilizing volunteers to restore natural spaces. Additionally, my involvement in a mentorship program for underprivileged youth allowed me to share knowledge, provide guidance, and inspire future leaders. Through these experiences, I witnessed the transformative power of community engagement and the positive impact it has on individuals and the collective well-being.",
            "Entrepreneurial spirit is evident in my initiatives to address real-world challenges. Founding a student-led startup, I developed and implemented innovative solutions to enhance campus sustainability. Through strategic planning, effective resource allocation, and collaboration with local businesses, I successfully launched eco-friendly initiatives that reduced our ecological footprint. This entrepreneurial journey sharpened my problem-solving skills, honed my ability to navigate uncertainties, and reinforced my commitment to creating positive change through innovative endeavors."
        ],
        "Institution": "University of Calgary",
        "Image": "data:image/png;base64,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",
        "Submitted": False,
        "Status": "accepted",
        "id": "1",
        "my_university": True
    }]

    # # Validate that username is present
    # if not username:
    #     return jsonify({'error': 'Invalid request. Missing username.'}), 400

    # docs = db.collection('users').document(username).collection('scholarship').get()
    # result = [doc.to_dict() for doc in docs]

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

        # Validate required fields
        if not username or not scholarship_title or index is None or updated_answer is None:
            return jsonify({'error': 'Invalid request. Missing required fields.'}), 400

        # Retrieve the scholarship document
        scholarship_ref = db.collection('users').document(username).collection('scholarship').document(scholarship_title)
        scholarship_doc = scholarship_ref.get().to_dict()

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
        request_message = f"The question asked in my scholarship application is this: {question} My Response is: {answer} Provide just the improved essay in about 100 words)"
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

@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        # Get data from the request
        data = request.json
        username = data.get('username')
        title = data.get('title')
        new_status = data.get('new_status')

        # Update user profile in the database
        db.collection('users').document(username).collection('scholarship').document(title).update({'Status':new_status})

        return jsonify({'success': True, 'message': 'User profile updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    conversations = [{"role": "system", "content": "You are a helpful assistant who specilaizes in enhancing users scholarship essays"}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversations
    )

    return jsonify({}), 200 


if __name__ == '__main__':
    app.run(debug=True)