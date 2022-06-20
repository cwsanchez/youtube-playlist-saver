from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database

engine = create_engine( 'sqlite:///playlist_data.db', echo=not True )

Session = sessionmaker()
Session.configure( bind=engine )
session = Session()

Base = declarative_base()

playlists_videos = Table(
    "playlists_videos",
    Base.metadata,
    Column( "playlistId", ForeignKey("playlists.id") ),
    Column( "videoId", ForeignKey("videos.id") )
)

class Playlist( Base ):
    __tablename__ = 'playlists'

    id = Column( String, primary_key=True )
    name = Column( String )
    description = Column( String )
    channelId = Column( String, ForeignKey("channels.id") )
    videos = relationship( "Video",  secondary=playlists_videos, backref="playlists" )

class Video( Base ):
    __tablename__ = 'videos'

    id = Column( String, primary_key=True )
    name = Column ( String )
    description = Column( String )
    channelId = Column( String, ForeignKey("channels.id") )

class Channel( Base ):
    __tablename__ = 'channels'

    id = Column( String, primary_key=True )
    name = Column( String )
    videos = relationship( "Video", backref="channel" )
    playlists = relationship( "Playlist", backref="channel" )

if not database_exists( engine.url ):
    Base.metadata.create_all( engine )
