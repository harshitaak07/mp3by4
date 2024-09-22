import requests
from bs4 import BeautifulSoup
import pyttsx3

def extract_text_from_webpage(url):
    """Extract text from the given webpage URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from paragraphs or other relevant tags
        text = ' '.join(p.get_text() for p in soup.find_all('p'))  # Extracts text from all <p> tags
        return text.strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def convert_text_to_speech(text, output_audio_file):
    """Convert the provided text to speech and save it as an audio file."""
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio_file)
    engine.runAndWait()

def main(url, output_audio_file):
    """Main function to extract text from a webpage and convert it to speech."""
    # Extract text from the webpage
    extracted_text = extract_text_from_webpage(url)
    
    if extracted_text:
        print("Extracted Text:")
        print(extracted_text)
        
        # Convert the extracted text to speech
        convert_text_to_speech(extracted_text, output_audio_file)
        print(f"TTS audio saved to: {output_audio_file}")
    else:
        print("No text extracted.")

if __name__ == "__main__":
    url = "https://example.com"  # Replace with your target webpage URL
    output_audio_file = "output_audio.mp3"
    output_audio_file = "C://Downloads/output_audio.mp3"

    main(url, output_audio_file)