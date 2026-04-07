import requests
import json

url = "http://172.25.107.226:5000/"
playlist_id = "PLTPM6TLvLmP1RmVBF3sM4kwv1MXtln09Z"
channel_id = "UClUXuLBYxXUt6X0HupY30rw"

selection = input( "\nWould you like to test a channel or playlist get request?\n" )

if selection == "channel":
    get_channel_request = requests.get(
            url + "channel/" + channel_id,
            headers={ 'Accept': 'application/json'}
    )

    print(
            f"Channel Get Results \nStatus Code: {get_channel_request.status_code}, "
            f"Response: {get_channel_request}"
    )
    try:
        print( f"JSON: {get_channel_request.json()}\n" )
    except:
        print( "\n" )
elif selection == "playlist":
    get_playlist_request = requests.get( 
            url + "playlist/" + playlist_id,
            headers={ 'Accept': 'application/json'}
    )

    print(
            f"Playlist Get Results \nStatus Code: {get_playlist_request.status_code}, "
            f"Response: {get_playlist_request}\n"
    )
    try:
        print( f"JSON: {get_playlist_request.json()}\n" )
    except:
        print( "\n" )
else:
    print( "Error, please select 'playlist' or 'channel'." )
