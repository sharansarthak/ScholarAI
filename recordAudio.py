# Handling recording on client side now so won't be needing this
import pyaudio
import wave
def record_audio(filename, duration):
    # Audio recording settings
    chunk = 1024
    fmt = pyaudio.paInt16
    channels = 1
    sample_rate = 44100

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=fmt, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk)

    print("Recording audio...")
    frames = []

    # Record for the set duration
    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(fmt))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))