import cv2
import numpy as np
import os

# Step 2: Set video file path
video_path = '/content/drive/MyDrive/19811797.mp4'  # Update with your video file name

# Step 3: Create output directory
output_dir = '/content/drive/My Drive/output_frames'
os.makedirs(output_dir, exist_ok=True)

# Load the video
cap = cv2.VideoCapture(video_path)
frame_count = 0
relevant_frames = []

# Initialize background subtractor
backSub = cv2.createBackgroundSubtractorMOG2()

# Pre-trained model for character detection
character_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    fg_mask = backSub.apply(frame)

    # Detect character
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    characters = character_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(characters) > 0:  # If character is detected
        # Create a mask for the detected character
        for (x, y, w, h) in characters:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around the character
            character_mask = np.zeros_like(frame)
            character_mask[y:y + h, x:x + w] = frame[y:y + h, x:x + w]  # Isolate character

            relevant_frames.append(character_mask)  # Keep only the character

    frame_count += 1

cap.release()

# Step 4: Create a new video from relevant frames
output_video_path = '/content/drive/My Drive/output_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
height, width, _ = relevant_frames[0].shape
out = cv2.VideoWriter(output_video_path, fourcc, 30, (width, height))

for frame in relevant_frames:
    out.write(frame)

out.release()

# Output confirmation
print(f'Video saved to: {output_video_path}')
