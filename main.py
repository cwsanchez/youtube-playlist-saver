from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort, fields, marshal_with
from playlistRequests import *
from sqlFunctions import *
from config import *
import json

app = Flask( __name__ )
api = Api( app )
api_key = SECRET_KEY

def addPlaylistData( playlist_id, api_key ):
    playlist_data = request_playlist( 
            playlist_id=playlist_id, 
            api_key=api_key 
    )
    addPlaylist( playlist_data )
    
    playlist_channel_id = playlist_data["items"][0]["snippet"]["channelId"]

    playlist_channel_data = request_channel(
        channel_id=playlist_channel_id,
        api_key=api_key
    )
    addChannel( channel_dict=playlist_channel_data )

    playlist_video_ids = request_playlist_videos(
        playlist_id=playlist_id,
        api_key=api_key
    )
    video_data = request_videos(
        video_ids=playlist_video_ids,
        api_key=api_key
    )
    addVideos( video_dicts=video_data )

    #print( '@addPlaylistData' )
    addNewVideosToPlaylist( 
        video_dicts=video_data,
        playlist_id=playlist_id
    )

class GetPlaylist(Resource):
    def get(self, playlist_id):
        playlist = getPlaylist( playlist_id=playlist_id )

        if playlist == None:
            abort( 404 )

        all_video_info = []

        for video in playlist.videos:
            video_info = {"id": video.id, "name": video.name, "channelId": video.channelId}  # Changed from flat list to dict list
            all_video_info.append(video_info)

        response = {
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "channelId": playlist.channelId,
            "videos": all_video_info
        }

        return response

class GetChannel(Resource):
    def get(self, channel_id):
        channel = getChannel( channel_id=channel_id )

        if channel == None:
            abort( 404 )

        all_playlist_ids = []
        for playlist in channel.playlists:
            all_playlist_ids.append(playlist.id)  # Fixed: was all_playlist_ids += playlist_id, which flattens string

        response = {
            "id": channel.id,
            "name": channel.name,
            "playlists": all_playlist_ids
        }

        return response

class AddPlaylist(Resource):
    def post(self):
        if request.method == "POST":
            playlist_id = request.json["id"]
            addPlaylistData(
                playlist_id=playlist_id,
                api_key=api_key
            )
        return '', 201

class AddChannel(Resource):
    def post(self):
        if request.method == "POST":
            channel_id = request.json["id"]
            channel_data = request_channel(
                channel_id=channel_id,
                api_key=api_key
            )
            addChannel( channel_dict=channel_data )

            channel_playlist_ids = request_channel_playlists(
                channel_id=channel_id,
                api_key=api_key
            )
            for playlist_id in channel_playlist_ids:
               addPlaylistData(
                   playlist_id=playlist_id,
                   api_key=api_key
                )
        return '', 201
            

api.add_resource( GetPlaylist, '/playlist/<string:playlist_id>' )
#api.add_resource( GetChannel, '/channel/<string:channel_id>' )
api.add_resource( AddPlaylist, '/playlist' )
api.add_resource( AddChannel, '/channel' )

def main():
    app.run( host='0.0.0.0', debug=True )
    
if __name__ == "__main__":
    main()
