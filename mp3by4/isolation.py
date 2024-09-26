import cv2
import mediapipe as mp
import numpy as np
import os
import shutil  
import subprocess   


def isolate_person(input_video, output_folder):
    # Initialize MediaPipe
    mp_selfie_segmentation = mp.solutions.selfie_segmentation

    # Clean up the output folder before processing
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)
    print(f"Opening video file: {input_video}")
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_video}")
        return 0    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Initialize frame counter
    frame_count = 0

    # Initialize the Selfie Segmentation model
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                break

            # Convert the BGR image to RGB and process it with MediaPipe Selfie Segmentation
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = selfie_segmentation.process(rgb_image)

            # Generate the segmentation mask
            mask = results.segmentation_mask

            # Refine the mask
            mask = cv2.GaussianBlur(mask, (7, 7), 0)
            mask = (mask > 0.1).astype(np.uint8) * 255

            # Convert back to RGBA image (keep the color in the right order, BGR to RGBA)
            rgba = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
            rgba[:, :, 3] = mask

            # Save the frame as a PNG file
            output_path = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
            cv2.imwrite(output_path, rgba)

            frame_count += 1

    # Release everything when done
    cap.release()
    cv2.destroyAllWindows()

    print(f"Processed {frame_count} frames. Output saved to {output_folder}")
    return fps

def stitch_images_to_video(image_folder, output_video, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    print(f"Found {len(images)} images in {image_folder}")
    images.sort()  # Ensure images are in the correct order

    if not images:
        print("No images found in the specified folder.")
        return

    # Read the first image to get dimensions
    frame = cv2.imread(os.path.join(image_folder, images[0]), cv2.IMREAD_UNCHANGED)
    height, width = frame.shape[:2]

    # Create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # You can also try 'avc1' or 'H264'
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        if frame.shape[2] == 4:  # If image has an alpha channel
            # Split the image into color channels and alpha channel
            b, g, r, a = cv2.split(frame)

            # Normalize alpha channel to float between 0 and 1
            alpha = a.astype(float) / 255.0

            # Convert the color channels to float for blending
            foreground = cv2.merge([r, g, b]).astype(float)  # Correct order: RGB

            # Ensure alpha is 3 channels to match the foreground
            alpha = np.dstack([alpha, alpha, alpha])

            # Create a white background
            white_bg = np.ones((height, width, 3), dtype=np.uint8) * 255

            # Resize the foreground to match the background (white_bg) size
            foreground = cv2.resize(foreground, (width, height))
            alpha = cv2.resize(alpha, (width, height))

            blended = foreground * alpha + white_bg * (1 - alpha)
            frame_bgr = blended.astype(np.uint8)
        else:
            frame_bgr = frame

        out.write(frame_bgr)

    out.release()
    print(f"Video created: {output_video}")



def reencode_video(input_video, audio_file, output_video):
    command = [
        'ffmpeg', '-y',  # Overwrite the output file
        '-i', input_video,
        '-c:v', 'libx264',  # Video codec H264
        '-crf', '23',  # Quality setting (lower is better, default is 23)
        '-preset', 'fast',  # Encoding speed vs. compression tradeoff
        '-pix_fmt', 'yuv420p',  # Ensures compatibility
        output_video
    ]
    subprocess.run(command)

def combine_audio_video(video_file, audio_file, output_file):
    command = [
        'ffmpeg', '-y',  # Overwrite the output file
        '-i', video_file,  # Input video file
        '-i', audio_file,  # Input audio file
        '-c:v', 'copy',  # Copy video codec
        '-c:a', 'aac',  # Set audio codec
        '-strict', 'experimental',  # Allow experimental codecs
        output_file  # Output file
    ]
    subprocess.run(command)
