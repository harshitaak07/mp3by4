import random
import google.generativeai as genai
import os
from datetime import datetime
import pyttsx3
import pyaudio
import wave
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_KEY')

# Generate lyrics using Gemini API
def generate_lyrics(input_text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Create a rap verse that incorporates the keywords. The lyrics should have a strong rhythm and flow, using internal rhymes and a consistent rhyme scheme. Make sure all the keywords are used naturally in the lyrics. The keywords are: " + input_text)
    print(response.text)
    return response.text

# Save to MP3 file and play using PyAudio
def save_to_mp3_and_play(lyrics):
    # Generate a unique filename using current timestamp
    filename = f"rap_song_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"

    # Initialize pyttsx3 for TTS
    engine = pyttsx3.init()

    # Set properties for voice
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name} - {voice.id}")

    # Select a male voice (you might need to adjust the index)
    male_voice_index = 0  # Adjust this based on the printed list
    engine.setProperty('voice', voices[male_voice_index].id)

    # Set speech rate (increase for faster speech)
    engine.setProperty('rate', 150)  # Adjust to your preference

    # Save the generated lyrics to an MP3 file
    engine.save_to_file(lyrics, filename)
    engine.runAndWait()

    print(f"Saved song as {filename}")

    # Play the MP3 file using PyAudio
    chunk = 1024  # Chunk size for audio stream
    wf = wave.open(filename, 'rb')  # PyAudio expects WAV; convert if needed
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks and play
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    input_text = "Hydrogen, Helium, Lithium, Beryllium, Carbon"
    generated_lyrics = generate_lyrics(input_text)
    
    # Save the song as MP3 and play it
    save_to_mp3_and_play(generated_lyrics)

if __name__ == "__main__":
    main()
