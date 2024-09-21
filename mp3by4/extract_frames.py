# extract_frames.py
import cv2

def extract_frames(video_path, output_folder='frames/'):
    cap = cv2.VideoCapture(video_path)
    frame_number = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_name = f'{output_folder}frame_{frame_number}.jpg'
        cv2.imwrite(frame_name, frame)
        print(f"Extracted: {frame_name}")
        frame_number += 1

    cap.release()
