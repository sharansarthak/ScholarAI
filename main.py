
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

@app.route('/process_media', methods=['POST'])
def process_media():
    media_path = request.json.get('media_path')
    audio_path = media_path.replace('.mp4', '.wav')  # Assuming .mp4, adjust as necessary

    # Extract audio from the video
    extract_audio_from_video(media_path, audio_path)

    # Now you can call your transcription function
    transcription = transcribe_audio(audio_path)  # Define this function based on your transcription logic

    return jsonify({"transcription": transcription})

