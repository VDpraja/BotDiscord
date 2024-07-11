from googleapiclient.discovery import build

def check_new_video(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=1,
        order="date"
    )
    response = request.execute()

    if response['items']:
        latest_video = response['items'][0]
        video_id = latest_video['id'].get('videoId')
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        title = latest_video['snippet']['title']
        thumbnail_url = latest_video['snippet']['thumbnails']['high']['url']
        return {
            "video_url": video_url,
            "title": title,
            "thumbnail_url": thumbnail_url
        }
    return None