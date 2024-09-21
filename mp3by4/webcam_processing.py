import cv2 
import numpy as np

global frame
global height
global width

# Function for horizontal, vertical, and diagonal sweeps
def HorVerDiagsweep():
    global frame
    global height
    global width
    
    delta = 20  # Adjusted for finer control
    frame = cv2.GaussianBlur(frame, (5, 5), 0)  # Optional noise reduction

    # Vertical and horizontal sweep
    for y in range(0, height-4):
        for x in range(0, width-4):
            cr, cg, cb = frame[y, x]
            Hr, Hg, Hb = frame[y, x+4]  # Horizontal
            Vr, Vg, Vb = frame[y+4, x]  # Vertical
            Dr, Dg, Db = frame[y+4, x+4]  # Diagonal
            
            # Check horizontal, vertical, and diagonal differences
            if abs(cr-Hr) > delta or abs(cg-Hg) > delta or abs(cb-Hb) > delta:
                frame[y, x] = (10, 10, 10)
            elif abs(cr-Vr) > delta or abs(cg-Vg) > delta or abs(cb-Vb) > delta:
                frame[y, x] = (10, 10, 10)
            elif abs(cr-Dr) > delta or abs(cg-Dg) > delta or abs(cb-Db) > delta:
                frame[y, x] = (10, 10, 10)
            else:
                frame[y, x] = (255, 255, 255)

# Function to capture a video from the webcam and save it
def getvideofile():
    global frame
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("Error: Unable to access the webcam.")
        return

    # Set capture properties for higher quality
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture.set(cv2.CAP_PROP_FPS, 30)

    writer = cv2.VideoWriter(
        "o1.avi",
        cv2.VideoWriter_fourcc(*'XVID'),  # Use XVID codec
        30,  # Higher frames per second
        (1920, 1080)  # Adjust to match resolution
    )
    
    i = 0
    while i < 100:
        flag, frame = capture.read()
        if not flag:
            break
        writer.write(frame)
        i += 1

    capture.release()
    writer.release()

# Function to process a video file
def processvideofile():
    global frame
    global height
    global width
    
    capture = cv2.VideoCapture("o1.avi")
    
    if not capture.isOpened():
        print("Error: Unable to open video file.")
        return

    flag, frame = capture.read()
    if not flag:
        print("Error: Unable to read from the video file.")
        return

    width1 = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    height = height1 - 1
    width = width1 - 1
    
    text = "Processed by NZee"
    
    writer = cv2.VideoWriter(
        "o2.avi",
        cv2.VideoWriter_fourcc(*'XVID'),  # Use XVID codec
        30,  # Higher frames per second
        (width1, height1)
    )
    
    i = 0
    while i < 100:
        print(f"Processing frame {i}")
        HorVerDiagsweep()
        
        # Enhanced text overlay
        cv2.putText(frame, text, (100, 50), fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=2, color=(255, 255, 255), thickness=2)
        writer.write(frame)
        
        flag, frame = capture.read()
        if not flag:
            break
        i += 1

    capture.release()
    writer.release()

# Start the video capture and processing
getvideofile()
processvideofile()