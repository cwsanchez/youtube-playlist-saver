from databaseSchema import *
import datetime
from sqlalchemy import insert, update

def queryPlaylistVideo( video_id, playlist_id ):
    with get_session() as sess:
        playlistsVideosQuery = sess.query( \
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
    with get_session() as sess:
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
        playlistQuery = sess.query( Playlist )
        playlist_result = playlistQuery.filter( Playlist.id == playlist_id ).first()
        playlist_video_results = queryPlaylistVideo( video_id=video_id, playlist_id=playlist_id )


        if playlist_video_results is None:
            # playlist_result.videos.append( video )

            # Corrected insert syntax for SQLAlchemy 2.x: use .values() method
            sess.execute(
                insert(playlists_videos).values(
                    [{"playlistId": playlist_id, "videoId": video_id, "removed_at": None}]
                )
            )
    #        print(
    #            100 * '=',
    #            '@addNewVideoToPlaylist',
    #            f"{playlist_result = }",
    #            f"{playlist_video_results = }",
    #            sep = "\n"
    #        )
            sess.commit()

def getPlaylist( playlist_id ):
    with get_session() as sess:
        playlistQuery = sess.query( Playlist )
        playlistIdQuery = playlistQuery.filter( Playlist.id == playlist_id ).first()

        return playlistIdQuery

def getChannel( channel_id ):
    with get_session() as sess:
        channelQuery = sess.query( Channel )
        channelIdQuery = channelQuery.filter( Channel.id == channel_id ).first()

        return channelIdQuery

def addVideo( video_dict, sess ):
    snippet = video_dict["snippet"]
    video_id = video_dict["id"]
    video_channel_name = snippet["channelTitle"]
    video_name = snippet["title"]
    video_description = snippet["description"]
    video_channel_id = snippet["channelId"]

    # Extract additional fields
    view_count = video_dict.get("statistics", {}).get("viewCount")
    view_count = int(view_count) if view_count else None
    like_count = video_dict.get("statistics", {}).get("likeCount")
    like_count = int(like_count) if like_count else None
    duration = video_dict.get("contentDetails", {}).get("duration")
    published_at_str = snippet.get("publishedAt")
    published_at = datetime.datetime.fromisoformat(published_at_str.replace("Z", "+00:00")) if published_at_str else None

    video = Video(
        id = video_id,
        name = video_name,
        description = video_description,
        channelId = video_channel_id,
        view_count = view_count,
        like_count = like_count,
        duration = duration,
        published_at = published_at
    )
    sess.merge( video )

def addVideos( video_dicts ):
    with get_session() as sess:
        items = video_dicts["items"]

        # Collect unique channels from videos
        unique_channels = {}
        for video in items:
            snippet = video["snippet"]
            ch_id = snippet["channelId"]
            ch_name = snippet["channelTitle"]
            if ch_id not in unique_channels:
                unique_channels[ch_id] = ch_name

        # Add channels first to satisfy foreign key constraint on videos.channelId
        for ch_id, ch_name in unique_channels.items():
            channel = Channel(id=ch_id, name=ch_name)
            sess.merge(channel)
        sess.commit()  # Commit channels before videos

        # Then add videos
        for video in items:
            addVideo(video_dict=video, sess=sess)  # Assumes addVideo does extraction and sess.merge(video), but no commit inside

        sess.commit()  # Commit videos after all are added

def addPlaylist( playlist_dict ):
    with get_session() as sess:
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
        sess.merge( playlist )
        sess.commit()

def addChannel( channel_dict ):
    with get_session() as sess:
        items = channel_dict["items"][0]
        snippet = items["snippet"]
        channel_id = items["id"]
        channel_name = snippet["title"]

        channel = Channel(
            id = channel_id,
            name = channel_name
        )
        sess.merge( channel )  # Use merge for upsert to handle duplicates gracefully
        sess.commit()

def get_all_channels():
    # New function: Returns all saved channels for dropdown population in Streamlit
    with get_session() as sess:
        return sess.query(Channel).all()

def get_all_playlists_for_channel(channel_id):
    # New function: Returns playlists for a given channel for browsing
    channel = getChannel(channel_id)
    return channel.playlists if channel else []

def refresh_playlist(playlist_id, api_key):
    with get_session() as sess:
        from playlistRequests import request_playlist, request_playlist_videos, request_videos
        # Fetch current
        playlist_data = request_playlist(playlist_id, api_key)  # To get channel etc if needed
        video_ids = request_playlist_videos(playlist_id, api_key)
        video_data = request_videos(video_ids, api_key)
        addVideos(video_data)  # Update/add videos
        # Get current active associations
        active_query = sess.query(playlists_videos).filter(playlists_videos.c.playlistId == playlist_id, playlists_videos.c.removed_at.is_(None))
        active_vids = [row.videoId for row in active_query.all()]
        # Mark removed
        for vid in active_vids:
            if vid not in video_ids:
                sess.execute(playlists_videos.update().where(playlists_videos.c.playlistId == playlist_id, playlists_videos.c.videoId == vid).values(removed_at=datetime.datetime.now()))
        # Add new
        for vid in set(video_ids) - set(active_vids):
            sess.execute(insert(playlists_videos).values({"playlistId": playlist_id, "videoId": vid, "removed_at": None}))
        sess.commit()
        # Update last_fetched
        playlist = getPlaylist(playlist_id)
        playlist.last_fetched = datetime.datetime.now()
        sess.commit()

def get_active_videos(playlist_id):
    with get_session() as sess:
        return sess.query(Video).join(playlists_videos).filter(playlists_videos.c.playlistId == playlist_id, playlists_videos.c.removed_at.is_(None)).all()

def get_removed_videos(playlist_id):
    with get_session() as sess:
        return sess.query(Video).join(playlists_videos).filter(playlists_videos.c.playlistId == playlist_id, playlists_videos.c.removed_at.isnot(None)).all()
