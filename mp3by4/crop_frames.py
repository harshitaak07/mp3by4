# crop_frames.py
import cv2

def crop_and_save_frame(frame, bbox, frame_id, output_folder='cropped_frames/'):
    x, y, w, h = bbox
    cropped_frame = frame[y:y+h, x:x+w]
    cv2.imwrite(f'{output_folder}cropped_frame_{frame_id}.jpg', cropped_frame)
    print(f"Saved cropped frame: cropped_frame_{frame_id}.jpg")
