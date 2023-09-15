
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean, select, insert, DateTime
from sqlalchemy.orm import Session, declarative_base, relationship, lazyload
from sqlalchemy.sql import func

from .write import CloneLogger

from datetime import datetime

Base = declarative_base()

# class Guild(Base):
#     __tablename__ = "guild"
#     id = Column(Integer, primary_key=True)
#     discord_id = Column(Integer, nullable=False, unique=True)
#     name = Column(String)

# class User(Base):
#     __tablename__ = "user"
#     id = Column(Integer, primary_key=True)
#     id_discord = Column(Integer, nullable=False, unique=True)
#     name = Column(String)

# class Channal(Base):
#     __tablename__ = "channal"
#     id = Column(Integer, primary_key=True)
#     id_discord = Column(Integer, nullable=False, unique=True)

#     # id_guild = Column(Integer,ForeignKey("guild.id_discord"))

#     name = Column(String)

class Action(Base):
    __tablename__ = "action"
    id = Column(Integer, primary_key=True)

    guild_id = Column(Integer)
    guild_name = Column(String)

    user_id = Column(Integer)
    user_name = Column(String)

    voice_before_id = Column(Integer)
    voice_before_name = Column(String)

    voice_after_id = Column(Integer)
    voice_after_name = Column(String)
    

    mute = Column(Boolean)
    deaf = Column(Boolean)
    stream = Column(Boolean)
    video = Column(Boolean)
    suppress = Column(Boolean)

    time = Column(DateTime(timezone=True), server_default=func.now())


class Message_action(Base):
    __tablename__ = "message_action"
    id = Column(Integer, primary_key=True)

    guild_id = Column(Integer)
    guild_name = Column(String)

    user_id = Column(Integer)
    user_name = Column(String)

    text = Column(String)
    
    time = Column(DateTime(timezone=True), server_default=func.now())

class createConnect():
    def __init__(
                self,
                connect_url: str = "sqlite:///voice.db",
            ):
        
        self.connect_url = connect_url
        self.Base = declarative_base()

        self.engine = create_engine(
            self.connect_url, 
            echo=False, 
            future=True
        )

        
        self.console_logger = CloneLogger(logger_name="db_module", console=True)

        self.session = Session(self.engine)
        self.conn_sqlalchemy = self.engine.connect()

        if not bool(self.engine.dialect.get_table_names(self.engine.connect())):
            print("create create all tables")
            Base.metadata.create_all(self.engine)

    def write_action(self, data:dict, console: bool = False):
        

        server:dict = data.get("server") # type: ignore
        user:dict = data.get("user")# type: ignore
        voice:dict = data.get("voice") # type: ignore
        before:dict = voice.get("before") # type: ignore
        after:dict = voice.get("after")  # type: ignore
        state:dict = data.get("state") # type: ignore

        action = Action(
            guild_id = server.get("id"),
            guild_name = server.get("name"),

            user_id = user.get("id"),
            user_name = user.get("name"),

            voice_before_id = before.get("id"),
            voice_before_name = before.get("name"),

            voice_after_id = after.get("id"),
            voice_after_name = after.get("name"),

            **state,

            time = datetime.now()
        )

        if console:
            self.console_logger.info(f"{server}\n{voice}\n{user}\n{state}\n")

        self.session.add(action)
        self.session.commit()

    def write_message(self, data:dict):


        server:dict = data.get("server") # type: ignore
        user:dict = data.get("user")# type: ignore
        text:dict = data.get("text") # type: ignore

        message = Message_action(
            guild_id = server.get("id"),
            guild_name = server.get("name"),

            user_id = user.get("id"),
            user_name = user.get("name"),

            text = text,
            time = datetime.now()
        )
        


        self.session.add(message)
        self.session.commit()

