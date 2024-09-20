# stitch_frames.py
import os
import cv2

def stitch_frames_to_video(output_video_path, frames_folder, fps=24):
    images = [f for f in os.listdir(frames_folder) if f.endswith(".jpg")]
    images.sort(key=lambda f: int(f.split('_')[2].split('.')[0]))  # Sort by frame number

    frame = cv2.imread(os.path.join(frames_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(frames_folder, image)))

    video.release()
    print(f"Video saved: {output_video_path}")
