# download_video.py
from pytube import YouTube

def download_video(video_url, output_path='videos/'):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    stream.download(output_path)
    print(f"Downloaded: {yt.title}")
