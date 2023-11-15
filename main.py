
import threading
from moviepy.editor import VideoFileClip, AudioFileClip
from flask import Flask, request, jsonify
import os
from speechToText import transcribe_audio
from recordAudio import record_audio
from recordVideo import record_video   
app = Flask(__name__)
from moviepy.editor import VideoFileClip, AudioFileClip
from speechToText import extract_audio_from_video, transcribe_audio
from openai import OpenAI
import os


# Read the API key from a file
with open("APIKEY", "r") as file:
    api_key = file.read().strip()

# Set the API key as an environment variable
os.environ["OPENAI_API_KEY"] = api_key

client = OpenAI()


@app.route('/process_media', methods=['POST'])
def process_media():
    media_path = request.json.get('media_path')
    audio_path = media_path.replace('.mp4', '.wav')  # Assuming .mp4, adjust as necessary

    # Extract audio from the video
    extract_audio_from_video(media_path, audio_path)

    # Now you can call your transcription function
    transcription = transcribe_audio(audio_path)  # Define this function based on your transcription logic

    return jsonify({"transcription": transcription})

@app.route('/request_chatgpt', methods=['POST'])
def chatgpt():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )

    print(response.choices[0].message.content)