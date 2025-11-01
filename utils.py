import re
import requests  # Assuming requests is already in deps
from playlistRequests import build_url  # Import build_url for handle resolution

def extract_playlist_id(url):
    # Extracts playlist ID from a YouTube URL or falls back to input if it's already an ID
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else url

def extract_channel_id(url, api_key):
    # Extracts channel ID from URL, handles /channel/UC... or @handle using YouTube API
    if '/channel/' in url:
        match = re.search(r'/channel/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)
    elif '@' in url:
        handle = url.split('@')[-1].split('/')[0]
        # Resolve handle to ID using API
        api_parts = ["id"]
        api_base_url = "https://www.googleapis.com/youtube/v3/channels"
        request_url = build_url(  # Assuming build_url is imported or accessible
            api_base_url=api_base_url,
            api_parts=api_parts,
            api_key=api_key,
            for_handle=f"@{handle}"
        )
        response = requests.get(request_url).json()
        if response.get("items"):
            return response["items"][0]["id"]
    return url  # Fallback if not a URL