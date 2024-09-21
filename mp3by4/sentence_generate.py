from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load the .env file
load_dotenv()

# Access the API key
api_key = os.getenv("GEMINI_KEY")

def query(input_text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Understand and generate a narration to teach the concepts given below. Make the explanation interesting and well structured. It is not necessary to use examples, but please use them if they help explain the topic better. Teach it to high schoolers and older age groups. Emphasise on using lesser metaphors, and generate the dialogue fluently. The concept basis is: "+input_text)
    print(response.text)

def main():
    with open('C:/Users/shamb/Downloads/extracted_text.txt', 'r',encoding='utf-8') as file:  # Ensure this matches where you save the file
        input_text = file.read()
    
    narrative = query(input_text)
    print(f"Narrative:\n{narrative}")
    

if __name__=="__main__":
    main()