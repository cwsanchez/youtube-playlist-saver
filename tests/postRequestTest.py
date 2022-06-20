import requests
import json

url = "http://172.25.107.226:5000"
playlist_id = "PLTPM6TLvLmP1RmVBF3sM4kwv1MXtln09Z"
channel_id = "UClUXuLBYxXUt6X0HupY30rw"

selection = input( "\nWould you like to test a channel or playlist post request?\n" )
if selection == "channel":
    channel_post_request = requests.post(
            url + "/channel",
            json={ "id": channel_id }
    )
    print(
        f"Channel Post Results \nStatus Code: {channel_post_request.status_code}, "
        f"Response: {channel_post_request}\n"
    )
elif selection == "playlist":
    playlist_post_request = requests.post(
            url + "/playlist",
            json={ "id": playlist_id }
    )
    print(
        f"\n\nPlaylist Post Results \nStatus Code: {playlist_post_request.status_code}, "
        f"Response: {playlist_post_request}\n"
    )
else:
    print( "\nOption invalid, must select 'playlist' or 'channel'.\n" )
