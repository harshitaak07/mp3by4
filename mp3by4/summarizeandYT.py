import os
import random
import yt_dlp
from googleapiclient.discovery import build
import cv2
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_KEY')
youtube_api_key = os.getenv('YT_KEY')


def summarize_text(input_text):
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = (
        "Summarize the following extracted content from a webpage into concise, well-organized notes. "
        "Focus on key points, important details, and main takeaways. The summary should be easy to review "
        "as study notes or a quick reference guide:\n\n"
        + input_text
    )
    
    response = model.generate_content(prompt)  
    return response.text

def search_youtube(query, max_results=1):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results
    ).execute()
    video_ids = [result['id']['videoId'] for result in search_response.get('items', []) if result['id']['kind'] == 'youtube#video']
    if video_ids:
        return f"https://www.youtube.com/watch?v={video_ids[0]}"
    else:
        print("No video found.")
        return None

def download_youtube_video(video_url, max_length_seconds, output_path='downloaded_video.mp4'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'match_filter': yt_dlp.utils.match_filter_func(f'!is_live & duration <= {max_length_seconds}')
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Video downloaded successfully: {output_path}")
    except Exception as e:
        print(f"Error downloading video: {e}")

def check_video_for_single_speaker(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file")
        return
    frame_count = 0
    single_face_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) == 1:
            single_face_count += 1
    cap.release()
    percentage_single_face = (single_face_count / frame_count) * 100
    print(f"Percentage of frames with a single person: {percentage_single_face:.2f}%")
    if percentage_single_face > 80:
        print("This video mostly focuses on one person.")
    else:
        print("This video may have multiple people or too much camera movement.")

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def calculate_video_length_based_on_summary(summary_text):
    
    return len(summary_text) * 2

# Main Process
if __name__ == '__main__':
    with open('C:/Users/eshit/Downloads/extracted_text.txt', 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    summary = summarize_text(extracted_text)
    print(f"Summary:\n{summary}")

    max_video_length_seconds = calculate_video_length_based_on_summary(summary)
    print(f"Max video length based on summary length: {max_video_length_seconds} seconds")

    office_characters = [
        "Michael Scott", "Dwight Schrute", "Jim Halpert", "Pam Beesly", 
        "Ryan Howard", "Kelly Kapoor", "Stanley Hudson", "Phyllis Vance", 
        "Angela Martin", "Kevin Malone", "Oscar Martinez", "Toby Flenderson", 
        "Creed Bratton", "Meredith Palmer", "Darryl Philbin", "Jan Levinson", 
        "Andy Bernard", "Erin Hannon", "Gabe Lewis", "Holly Flax"
    ]

    selected_character = random.choice(office_characters)
    print(f"Randomly selected character: {selected_character}")

    search_query = f"{selected_character} monologue The Office"

    video_url = search_youtube(search_query)

    if video_url:
        print(f"Found video: {video_url}")
        download_youtube_video(video_url, max_video_length_seconds)

        check_video_for_single_speaker('downloaded_video.mp4')
