# Youtube Playlist Saver
API that saves Youtube playlist data to a database and can return it when queried. 
I plan on eventually adding a front end that shows you which videos have been deleted since the playlist was added.

To start the app run:

```
pip3 install -r requirements.txt
python3 main.py
```

Get request for playlist info:

```
GET /playlist/<playlist_id>
```

Post request for submitting playlist info:

```
POST /playlist

{ id: <playlist_id }
```

Post request for submitting all playlists for a channel:

```
POST /channel

{ id: <channel_id> }
```
