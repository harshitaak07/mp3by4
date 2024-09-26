from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def combine_audio_video(video_path, audio_path, output_path):
    try:
        # Load the video and audio clips
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # If audio is longer than video, loop the video
        if audio.duration > video.duration:
            num_loops = int(audio.duration / video.duration) + 1
            video = concatenate_videoclips([video] * num_loops)
            video = video.subclip(0, audio.duration)
        else:
            # If video is longer, trim it to match audio length
            video = video.subclip(0, audio.duration)

        # Set the audio of the video clip
        final_clip = video.set_audio(audio)

        # Write the result to a file
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

        print(f"Video successfully saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if 'video' in locals():
            video.close()
        if 'audio' in locals():
            audio.close()
        if 'final_clip' in locals():
            final_clip.close()

