import cv2
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit

video_path = 'hello.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

if not out.isOpened():
    print("Error: Could not open output video file for writing.")
    exit()

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    _, mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    white_background = np.full_like(frame, 255)  
    
    mask_inv = cv2.bitwise_not(mask)
    
    foreground = cv2.bitwise_and(frame, frame, mask=mask)
    
    background = cv2.bitwise_and(white_background, white_background, mask=mask_inv)
    
    result = cv2.add(foreground, background)
    
    return result

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Finished processing all frames or error reading the video.")
        break
    
    print(f"Processing frame of size {frame.shape}")
    
    processed_frame = process_frame(frame)
    
    cv2.imshow('Processed Frame', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    out.write(processed_frame)

cap.release()
out.release()
cv2.destroyAllWindows()
