import os
from google.cloud import speech

# Set the path to the credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ace-axon-345319-373465ce4bf2.json"

from moviepy.editor import VideoFileClip
import subprocess


def extract_audio(video_path, audio_path, audio_format="mp3"):
    try:
        ffmpeg_command = ["ffmpeg", "-y", "-i", video_path]

        if audio_format == "mp3":
            ffmpeg_command.extend(["-q:a", "0", "-map", "a", audio_path])
        elif audio_format == "wav":
            ffmpeg_command.extend(["-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_path])

        subprocess.run(ffmpeg_command, check=True)
        print(f"Audio extracted successfully to {audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}")


def extract_audio_from_video(video_path, audio_path):
    print(f"Extracting audio from: {video_path} to {audio_path}")

    try:
        with VideoFileClip(video_path) as video_clip:
            if video_clip.audio is None:
                print("No audio found in the video clip.")
                return False
            video_clip.audio.write_audiofile(audio_path)
        
        print(f"Audio extracted successfully to {audio_path}")
        return True
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return False

def transcribe_audio(speech_file):
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-IN",
        enable_automatic_punctuation=True
    )


    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
