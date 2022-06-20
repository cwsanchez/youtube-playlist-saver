import json
import requests

def build_url( 
        api_base_url, 
        api_parts, 
        api_key, 
        resource_id=None, 
        playlist_id=None,
        channel_id=None,
        max_results=None,
        video_ids=None
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
    channel_data = json.loads( json_channel.text )

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
    channel_playlist_data = json.loads( json_channel_playlists.text )

    return channel_playlist_data

def request_channel_all_items( channel_id, api_key, max_results ):
    request_headers = { "Accept": "application/json" }
    api_parts = [ "id" ]
    api_base_url = "https://www.googleapis.com/youtube/v3/playlists"

    request_url = build_url(
        api_base_url = api_base_url,
        api_parts = api_parts,
        channel_id = channel_id,
        api_key = api_key,
        max_results = max_results
    )

    json_channel_all_playlists = requests.get(
        request_url,
        headers = request_headers
    )
    channel_playlist_all_data = json.loads( json_channel_all_playlists.text )

    return channel_playlist_all_data

def request_channel_playlists( channel_id, api_key ):
    channel_playlist_data = request_channel_items( 
        channel_id = channel_id,
        api_key = api_key
    )

    itemCount = channel_playlist_data["pageInfo"]["totalResults"]

    channel_all_playlist_data = request_channel_all_items( 
        channel_id=channel_id,
        api_key=api_key,
        max_results=itemCount
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
    playlist_data = json.loads( json_playlist.text )

    return playlist_data

def request_playlist_items( playlist_id, api_key, max_results ):
    request_headers = { "Accept": "application/json" }
    api_parts = [ "contentDetails" ]
    api_base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    
    request_url = build_url( 
        api_base_url = api_base_url,
        api_parts = api_parts,
        playlist_id = playlist_id,
        api_key = api_key,
        max_results = max_results
    )

    json_playlist = requests.get(
        request_url,
        headers = request_headers
    )
    playlist_data = json.loads( json_playlist.text )

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
            max_results = itemCount
    )

    video_ids = []
   
    for video in playlist_data["items"]: 
        if video["kind"] == "youtube#playlistItem":
            video_ids.append( video["contentDetails"]["videoId"] )

    return video_ids

def request_videos( video_ids, api_key ):
    request_headers = { "Accept": "application/json" }
    api_parts = ["snippet", "contentDetails", "statistics", "recordingDetails", "topicDetails"]
    api_base_url = "https://www.googleapis.com/youtube/v3/videos" 

    request_url = build_url( 
        api_base_url = api_base_url,
        api_parts = api_parts,
        api_key = api_key,
        video_ids = video_ids
    )

    json_video = requests.get(
            request_url,
            headers = request_headers
    )
    video_data = json.loads( json_video.text )

    return video_data

def request_multiple_playlists_videos( playlist_ids, api_key ):
    playlists = []

    for playlist in playlist_ids:
        playlist_data = request_playlist_videos(
            playlist_id = playlist,
            api_key = api_key
        )
        playlists.append( playlist_data )
    
    return playlists
