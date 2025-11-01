import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database

db_url = st.secrets.get("DATABASE_URL", 'sqlite:///playlist_data.db')  # Fallback to local SQLite if no secret
engine = create_engine(db_url, echo=False, pool_pre_ping=True)  # Add pool_pre_ping for cloud Postgres resilience

Session = sessionmaker()
Session.configure( bind=engine )
session = Session()

Base = declarative_base()

playlists_videos = Table(
    "playlists_videos",
    Base.metadata,
    Column( "playlistId", ForeignKey("playlists.id") ),
    Column( "videoId", ForeignKey("videos.id") ),
    Column("removed_at", DateTime, nullable=True)
)

class Playlist( Base ):
    __tablename__ = 'playlists'

    id = Column( String, primary_key=True )
    name = Column( String )
    description = Column( String )
    channelId = Column( String, ForeignKey("channels.id") )
    last_fetched = Column(DateTime, nullable=True)
    videos = relationship( "Video",  secondary=playlists_videos, backref="playlists" )

class Video( Base ):
    __tablename__ = 'videos'

    id = Column( String, primary_key=True )
    name = Column ( String )
    description = Column( String )
    channelId = Column( String, ForeignKey("channels.id") )
    view_count = Column(Integer, nullable=True)
    like_count = Column(Integer, nullable=True)
    duration = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)

class Channel( Base ):
    __tablename__ = 'channels'

    id = Column( String, primary_key=True )
    name = Column( String )
    videos = relationship( "Video", backref="channel" )
    playlists = relationship( "Playlist", backref="channel" )

# For SQLite only: if not database_exists(engine.url): Base.metadata.create_all(engine)
Base.metadata.create_all(engine)  # Safe for existing tables
