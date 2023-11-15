import os
from google.cloud import speech

# Set the path to the credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ace-axon-345319-373465ce4bf2.json"

def transcribe_audio(speech_file):
    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# Example usage
transcribe_audio("output_audio.wav")
