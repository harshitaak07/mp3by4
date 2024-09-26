import requests
from bs4 import BeautifulSoup
import pyttsx3
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_KEY')

def summarize_text(input_text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Understand and generate a detailed narration to teach the concepts given below. Make the explanation interesting and well structured. It is not necessary to use examples, but please use them if they help explain the topic better. Teach it to high schoolers and older age groups. Emphasise on using lesser metaphors, and generate the dialogue fluently. DO NOT GENERATE POINTS.  The concept basis is:" + input_text)
    print(response)
    return response.text

def extract_text_from_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.content, 'html.parser')

        text = ' '.join(p.get_text() for p in soup.find_all('p'))  # Extracts text from all <p> tags
        return text.strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def convert_text_to_speech(text, output_audio_file, speed=100):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio_file)
    engine.runAndWait()

def main(url, output_audio_file):
    extracted_text = extract_text_from_webpage(url)
    summary = summarize_text(extracted_text)
    
    if extracted_text:
        print("Extracted Text:")
        print(summary)
        
        convert_text_to_speech(summary, output_audio_file, speed=100)
        print(f"TTS audio saved to: {output_audio_file}")
    else:
        print("No text extracted.")

if __name__ == "__main__":
    url = "https://www.geeksforgeeks.org/cloud-computing/"  
    output_audio_file = "output_audio.mp3"
    output_audio_file = "C://Downloads/output_audio.mp3"

    main(url, output_audio_file)