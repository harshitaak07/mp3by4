import os
import googleapiclient.discovery
import yt_dlp as youtube_dl 

API_KEY = 'AIzaSyBE5kLU3xYeklLYytBOJ0ZncvCJUM1tGiA'

def search_youtube(query, max_results=5):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results,
        order="relevance"
    )
    
    response = request.execute()
    
    video_results = []
    for item in response['items']:
        video_id = item['id']['videoId']
        
        video_request = youtube.videos().list(
            part="contentDetails",
            id=video_id
        )
        video_response = video_request.execute()
        
        duration = video_response['items'][0]['contentDetails']['duration']
        duration_seconds = parse_duration(duration)
        
        if duration_seconds <= 200:  #timelimit if video
            video_data = {
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'video_id': video_id,
                'description': item['snippet']['description'],
                'published_at': item['snippet']['publishedAt'],
                'duration': duration_seconds
            }
            video_results.append(video_data)
    
    return video_results

def parse_duration(duration):
    import isodate
    return int(isodate.parse_duration(duration).total_seconds())

def download_video(video_url, save_path='.'):
    ydl_opts = {
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'format': 'best',
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading: {video_url}")
        ydl.download([video_url])
        print("Download complete.")

def main():
    query = input("Enter a search query (e.g., The Office characters): ")
    results = search_youtube(query, max_results=10)  
    
    print(f"Top {len(results)} results for '{query}':\n")
    
    for idx, video in enumerate(results):
        print(f"{idx + 1}. {video['title']} (Duration: {video['duration']} seconds)")
        print(f"   URL: {video['url']}")
        print(f"   Published at: {video['published_at']}")
        print(f"   Description: {video['description']}\n")
    
    if results:
        download_choice = input("Do you want to download the first video? (yes/no): ").strip().lower()
        if download_choice == 'yes':
            video_url = results[0]['url']
            save_path = '.'
            download_video(video_url, save_path)

if __name__ == "__main__":
    main()
