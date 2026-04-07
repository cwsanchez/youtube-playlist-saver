import json
import requests
import time

def chunks(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def build_url(
        api_base_url,
        api_parts,
        api_key,
        resource_id=None,
        playlist_id=None,
        channel_id=None,
        max_results=None,
        video_ids=None,
        for_handle=None
):
    api_part_url = ""
    api_key = f"&key={api_key}"

    for index, part in enumerate( api_parts ):
        if index == 0:
            api_part_url += f"?part={part}"
        else:
            api_part_url += f"%2C{part}"

    request_url = ( f"{api_base_url}{api_part_url}{api_key}" )

    if resource_id != None:
        request_url += f"&id={resource_id}"

    if playlist_id != None:
        request_url += f"&playlistId={playlist_id}"

    if channel_id != None:
        request_url += f"&channelId={channel_id}"

    if max_results != None:
        request_url += f"&maxResults={max_results}"

    if video_ids != None:
        video_ids_url = ""
        for index, video in enumerate(video_ids):
            if index == 0:
                video_ids_url += f"&id={video}"
            else:
                video_ids_url += f"%2C{video}"
        request_url += video_ids_url

    if for_handle is not None:
        request_url += f"&forHandle={for_handle}"  # Added support for channel handles like @username

    return request_url

def request_channel( channel_id, api_key ):
    request_headers = { "Accept": "application/json" }
    api_parts = [ "id", "snippet" ]
    api_base_url = "https://www.googleapis.com/youtube/v3/channels"

    request_url = build_url( 
        api_base_url = api_base_url,
        api_parts = api_parts,
        resource_id = channel_id,
        api_key = api_key
    )

    json_channel = requests.get(
        request_url,
        headers = request_headers
    )
    time.sleep(0.5)
    channel_data = json.loads( json_channel.text )

    # Check for API error in response
    if "error" in channel_data:
        error = channel_data["error"]
        raise ValueError(f"YouTube API error: {error.get('code', 'Unknown')} - {error.get('message', 'No message')}")

    return channel_data

def request_channel_items( channel_id, api_key ):
    request_headers = { "Accept": "application/json" }
    api_parts = [ "id" ]
    api_base_url = "https://www.googleapis.com/youtube/v3/playlists"

    request_url = build_url(
        api_base_url = api_base_url,
        api_parts = api_parts,
        channel_id = channel_id,
        api_key = api_key
    )

    json_channel_playlists = requests.get(
        request_url,
        headers = request_headers
    )
    time.sleep(0.5)
    channel_playlist_data = json.loads( json_channel_playlists.text )

    # Check for API error in response
    if "error" in channel_playlist_data:
        error = channel_playlist_data["error"]
        raise ValueError(f"YouTube API error: {error.get('code', 'Unknown')} - {error.get('message', 'No message')}")

    return channel_playlist_data

def request_channel_all_items( channel_id, api_key ):
    # Added pagination to handle large channel playlists, always fetch all with per_page=50 to respect API limits (maxResults 0-50 per page)
    request_headers = { "Accept": "application/json" }
    api_parts = [ "id" ]
    api_base_url = "https://www.googleapis.com/youtube/v3/playlists"

    per_page = 50
    remaining = float('inf')
    all_items = []
    page_token = None

    while True:
        request_url = build_url(
            api_base_url = api_base_url,
            api_parts = api_parts,
            channel_id = channel_id,
            api_key = api_key,
            max_results = min(per_page, remaining)
        )
        if page_token:
            request_url += f"&pageToken={page_token}"

        json_channel_all_playlists = requests.get(
            request_url,
            headers = request_headers
        )
        time.sleep(0.5)
        channel_playlist_all_data = json.loads( json_channel_all_playlists.text )

        # Check for API error in response
        if "error" in channel_playlist_all_data:
            error = channel_playlist_all_data["error"]
            raise ValueError(f"YouTube API error: {error.get('code', 'Unknown')} - {error.get('message', 'No message')}")

        all_items.extend(channel_playlist_all_data.get("items", []))
        remaining -= len(channel_playlist_all_data.get("items", []))
        page_token = channel_playlist_all_data.get("nextPageToken")
        if not page_token or remaining <= 0:
            break

    # Return in the same format as before
    channel_playlist_all_data["items"] = all_items
    return channel_playlist_all_data

def request_channel_playlists( channel_id, api_key ):
    channel_playlist_data = request_channel_items(
        channel_id = channel_id,
        api_key = api_key
    )

    itemCount = channel_playlist_data["pageInfo"]["totalResults"]

    channel_all_playlist_data = request_channel_all_items(
        channel_id=channel_id,
        api_key=api_key
    )

    playlist_ids = []

    for video in channel_all_playlist_data["items"]:
        if video["kind"] == "youtube#playlist":
            playlist_ids.append( video["id"] )

    return playlist_ids

def request_playlist( playlist_id, api_key):
    request_headers = { "Accept": "application/json" }
    api_parts = [ "contentDetails", "id", "snippet" ] 
    api_base_url = "https://www.googleapis.com/youtube/v3/playlists"

    request_url = build_url( 
        api_base_url = api_base_url,
        api_parts = api_parts,
        resource_id = playlist_id,
        api_key = api_key
    )

    json_playlist = requests.get(
        request_url,
        headers = request_headers
    )
    time.sleep(0.5)
    playlist_data = json.loads( json_playlist.text )

    # Check for API error in response
    if "error" in playlist_data:
        error = playlist_data["error"]
        raise ValueError(f"YouTube API error: {error.get('code', 'Unknown')} - {error.get('message', 'No message')}")

    return playlist_data

def request_playlist_items( playlist_id, api_key, max_results ):
    request_headers = { "Accept": "application/json" }
    api_parts = [ "contentDetails" ]
    api_base_url = "https://www.googleapis.com/youtube/v3/playlistItems"

    # Set per_page = 50 to respect API limits (maxResults 0-50 per page)
    per_page = 50
    remaining = max_results if max_results else float('inf')
    all_items = []
    page_token = None

    while True:
        request_url = build_url(
            api_base_url = api_base_url,
            api_parts = api_parts,
            playlist_id = playlist_id,
            api_key = api_key,
            max_results = min(per_page, remaining)
        )
        if page_token:
            request_url += f"&pageToken={page_token}"

        json_playlist = requests.get(
            request_url,
            headers = request_headers
        )
        time.sleep(0.5)
        playlist_data = json.loads( json_playlist.text )

        # Check for API error in response
        if "error" in playlist_data:
            error = playlist_data["error"]
            raise ValueError(f"YouTube API error: {error.get('code', 'Unknown')} - {error.get('message', 'No message')}")

        all_items.extend(playlist_data.get("items", []))
        remaining -= len(playlist_data.get("items", []))
        page_token = playlist_data.get("nextPageToken")
        if not page_token or remaining <= 0:
            break

    playlist_data["items"] = all_items
    return playlist_data

def request_playlist_videos( playlist_id, api_key ):
    playlist_data = request_playlist(
            playlist_id = playlist_id,
            api_key = api_key
    )

    itemCount = playlist_data["items"][0]["contentDetails"]["itemCount"]

    playlist_data = request_playlist_items(
            playlist_id = playlist_id,
            api_key = api_key,
            max_results = None
    )

    video_ids = []

    for video in playlist_data["items"]:
        if video["kind"] == "youtube#playlistItem":
            video_ids.append( video["contentDetails"]["videoId"] )

    return video_ids

def request_videos( video_ids, api_key ):
    if not video_ids:
        return {"items": []}

    request_headers = { "Accept": "application/json" }
    api_parts = ["snippet", "contentDetails", "statistics", "recordingDetails", "topicDetails"]
    api_base_url = "https://www.googleapis.com/youtube/v3/videos"

    all_items = []

    for chunk in chunks(video_ids, 50):
        request_url = build_url(
            api_base_url = api_base_url,
            api_parts = api_parts,
            api_key = api_key,
            video_ids = chunk
        )

        json_video = requests.get(
            request_url,
            headers = request_headers
        )
        time.sleep(0.5)
        video_data = json.loads( json_video.text )

        # Check for API error in response
        if "error" in video_data:
            error = video_data["error"]
            raise ValueError(f"YouTube API error: {error.get('code', 'Unknown')} - {error.get('message', 'No message')}")

        all_items.extend(video_data.get("items", []))

    return {"items": all_items}

def request_multiple_playlists_videos( playlist_ids, api_key ):
    playlists = []

    for playlist in playlist_ids:
        playlist_data = request_playlist_videos(
            playlist_id = playlist,
            api_key = api_key
        )
        playlists.append( playlist_data )
    
    return playlists
