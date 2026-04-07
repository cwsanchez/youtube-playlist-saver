from typing import List
from pydantic import BaseModel


API_BASE_URL= "https://foo.bar.com"
API_KEY = "awureothopawireht"
HEADERS = { "Accept": "application/json" }

class Url( BaseModel ) :


    resource_id : str
    playlist_id : str
    max_results : int
    video_ids : List[str]
    api_base_url : str
    api_parts : List[str]

    def build( self ) :

        api_part_url = ""
        api_key = f"&key={API_KEY}"

        for index, part in enumerate( self.api_parts ):
            if index == 0:
                api_part_url += f"?part={part}"
            else:
                api_part_url += f"%2C{part}"

        request_url = ( f"{api_base_url}{api_part_url}{api_key}" )

        if self.resource_id != None:
            request_url += f"&id={self.resource_id}"

        if self.playlist_id != None:
            request_url += f"&playlistId={self.playlist_id}"

        if self.channel_id != None:
            request_url += f"&channelId={self.channel_id}"

        if self.max_results != None:
            request_url += f"&maxResults={self.max_results}"

        if self.video_ids != None:
            video_ids_url = ""
            for index, video in enumerate(self.video_ids):
                if index == 0:
                    video_ids_url += f"&id={video}"
                else:
                    video_ids_url += f"%2C{video}"
            request_url += video_ids_url

        return request_url

def request_channel( url : Url ):
    """Accepts a Url object and requests some channel data"""

    request_url = url.build()

    json_channel = requests.get(
        request_url,
        headers = request_headers
    )
    channel_data = json.loads( json_channel.text )

    return channel_data



class Queries :
    """Use this to group together similar functions with similar arguments.
    Just for convenience.

    Queries.queryPlaylistsVideos
    """
    @staticmethod
    def queryPlaylistsVideos( video_id, playlist_id ):
        playlistsVideosQuery = session.query \
            .join( playlists_videos ) \
            .join( Playlists ) \
            .filter(
                (playlists_videos.c.videoId == video_id ) &
                (playlists_videos.c.playlistId == playlist_id )
            ) \
            .first()

        return playlistsVideoQuery


