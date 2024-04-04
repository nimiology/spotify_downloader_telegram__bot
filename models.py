from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine(f'sqlite:///database.db')
Base = declarative_base()


# Define the User table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)


# Define the Song table
class SongRequest(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    spotify_id = Column(String, nullable=False)
    song_id_in_group = Column(Integer)
    group_id = Column(Integer)
    user = relationship('User', backref='songs')


# Create the tables in the database if they don't exist
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
