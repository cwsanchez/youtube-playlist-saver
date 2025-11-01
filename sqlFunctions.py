from databaseSchema import *

def queryPlaylistVideo( video_id, playlist_id ):
    playlistsVideosQuery = session.query( \
        #Video.id, Playlist.id, '
            playlists_videos \
        ) \
        .filter( playlists_videos.c.videoId == video_id ) \
        .filter( playlists_videos.c.playlistId == playlist_id ) \
        .first()

    return playlistsVideosQuery

def addNewVideosToPlaylist( video_dicts, playlist_id ):
    items = video_dicts["items"]
    for video in items:
        addNewVideoToPlaylist( video_dict=video, playlist_id=playlist_id )

def addNewVideoToPlaylist( video_dict, playlist_id ):
    snippet = video_dict["snippet"]
    video_id = video_dict["id"]
    video_name = snippet["title"]
    video_description = snippet["description"]
    video_channel_id = snippet["channelId"]

    video = Video(
        id = video_id,
        name = video_name,
        description = video_description,
        channelId = video_channel_id
    )

    # Query playlist-videos
    playlistQuery = session.query( Playlist )
    playlist_result = playlistQuery.filter( Playlist.id == playlist_id ).first()
    playlist_video_results = queryPlaylistVideo( video_id=video_id, playlist_id=playlist_id )

    
    if playlist_video_results is None:
        # playlist_result.videos.append( video )

        # Corrected insert syntax for SQLAlchemy 2.x: use .values() method
        from sqlalchemy import insert
        session.execute(
            insert(playlists_videos).values(
                [{"playlistId": playlist_id, "videoId": video_id}]
            )
        )
#        print( 
#            100 * '=', 
#            '@addNewVideoToPlaylist', 
#            f"{playlist_result = }", 
#            f"{playlist_video_results = }", 
#            sep = "\n" 
#        )
        session.commit()

def getPlaylist( playlist_id ):
    playlistQuery = session.query( Playlist )
    playlistIdQuery = playlistQuery.filter( Playlist.id == playlist_id ).first()

    return playlistIdQuery

def getChannel( channel_id ):
    channelQuery = session.query( Channel )
    channelIdQuery = channelQuery.filter( Channel.id == channel_id ).first()
    
    return channelIdQuery

def addVideo( video_dict ):
    snippet = video_dict["snippet"]
    video_id = video_dict["id"]
    video_channel_name = snippet["channelTitle"]
    video_name = snippet["title"]
    video_description = snippet["description"]
    video_channel_id = snippet["channelId"]

    video = Video(
        id = video_id,
        name = video_name,
        description = video_description,
        channelId = video_channel_id
    )
    session.merge( video )
    session.commit()

def addVideos( video_dicts ):
    items = video_dicts["items"]
    for video in items:
        addVideo( video_dict=video )

def addPlaylist( playlist_dict ):
    items = playlist_dict["items"][0]
    snippet = items["snippet"]
    playlist_id = items["id"]
    playlist_name = snippet["title"]
    playlist_description = snippet["description"]
    playlist_channel_id = snippet["channelId"]

    playlist = Playlist(
        id = playlist_id,
        name = playlist_name,
        description = playlist_description,
        channelId = playlist_channel_id
    )
    session.merge( playlist )
    session.commit()

def addChannel( channel_dict ):
    items = channel_dict["items"][0]
    snippet = items["snippet"]
    channel_id = items["id"]
    channel_name = snippet["title"]

    channel = Channel(
        id = channel_id,
        name = channel_name
    )
    session.merge( channel )  # Use merge for upsert to handle duplicates gracefully
    session.commit()

def get_all_channels():
    # New function: Returns all saved channels for dropdown population in Streamlit
    return session.query(Channel).all()

def get_all_playlists_for_channel(channel_id):
    # New function: Returns playlists for a given channel for browsing
    channel = getChannel(channel_id)
    return channel.playlists if channel else []
