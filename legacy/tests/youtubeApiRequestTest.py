from playlistRequests import *

def main():
    playlist_id = "PLTPM6TLvLmP3RYMqLw_2eoyD1JhmacVhb"
    various_playlists = [ 
            "PLTPM6TLvLmP3RYMqLw_2eoyD1JhmacVhb", 
            "PLTPM6TLvLmP3Vrks1zuK7mlp2fZhCzMcK",
            "PLTPM6TLvLmP2GRtT-mOGcgSbUrQaycGs7"
    ]
    channel_id = "UClUXuLBYxXUt6X0HupY30rw"
    api_key = "AIzaSyCQygOajsSBDSS0_SQrMef31rytxP80i80"
    max_results = 1

    playlist = request_playlist(
        playlist_id = playlist_id,
        api_key = api_key,
    )

    playlist_video_ids = request_playlist_items(
        playlist_id = playlist_id, 
        api_key = api_key,
        max_results = max_results
    )

    playlist_videos = request_playlist_videos(
        playlist_id = playlist_id,
        api_key = api_key
    )

    videos = request_videos(
        video_ids = playlist_videos,
        api_key = api_key
    )

    channel = request_channel( 
        channel_id = channel_id, 
        api_key = api_key
    )
    
    channel_playlist_ids = request_channel_playlists(
        channel_id = channel_id,
        api_key = api_key
    )

    multiple_playlists_videos = request_multiple_playlists_videos( 
        playlist_ids = various_playlists,
        api_key = api_key
    )

    while True:
        try:
            test = locals()[
                    input( "What would you like to test? (playlist, playlist_videos, playlist_video_ids, videos, channel, channel_playlist_ids, multiple_playlists_videos): "  )
            ]
            
            print( f"\n{test}\n" )
            break
        except KeyError:
            print( "\nPlease specify playlist, playlist_videos, playlist_video_ids, videos, channel, channel_playlist_ids, or multiple_playlists_videos.\n" )
      


main()
