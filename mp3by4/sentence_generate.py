from dotenv import load_dotenv
import google.generativeai as genai
import os
import re
import wave
import pyaudio
import pyttsx3
from datetime import datetime

# Load the .env file
load_dotenv()

# Access the API key
api_key = os.getenv("GEMINI_KEY")

def query(input_text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Understand and generate a narration to teach the concepts given below. Make the explanation interesting and well structured. It is not necessary to use examples, but please use them if they help explain the topic better. Teach it to high schoolers and older age groups. Emphasise on using lesser metaphors, and generate the dialogue fluently. Do not use bolds or italics. The concept basis is: "+input_text)
    narrative = ""
    for lex in response.text:
        if (lex=="*" or lex=="#"):
            continue
        else:
            narrative+=lex
    return (narrative)

def save_to_mp3_and_play(lyrics):
    
    filename = f"video_narrative.mp3"

    # Initialize pyttsx3 for TTS
    engine = pyttsx3.init()

    # Set properties for voice
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}: {voice.name} - {voice.id}")

    # Select a male voice (you might need to adjust the index)
    male_voice_index = 0  # Adjust this based on the printed list
    engine.setProperty('voice', voices[male_voice_index].id)

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
    with open(r'C:\Users\devis\Downloads\extracted_text.txt', 'r', encoding='utf-8') as file:  # Ensure this matches where you save the file
        input_text = file.read()
    
    narrative = query(input_text)
    print(f"Narrative:\n{narrative}")
    save_to_mp3_and_play(narrative)


if __name__=="__main__":
    main()