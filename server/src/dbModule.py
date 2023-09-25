
from sqlalchemy import Table, BIGINT, BOOLEAN, VARCHAR, MetaData, create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql import func
# from .schemes import ActionClass

from datetime import datetime

Base = declarative_base()
metadata = MetaData()

class ActionClass(Base):
    __tablename__ = 'ActionTable'
    id = Column('id', BIGINT(), autoincrement=True, primary_key=True, nullable=False)
    guild_id = Column('guild_id', BIGINT(), nullable=False, autoincrement=False)
    guild_name = Column('guild_name', VARCHAR(255), nullable=False, autoincrement=False)
    user_id = Column('user_id', BIGINT(), nullable=False, autoincrement=False)
    user_name = Column('user_name', VARCHAR(255), nullable=False, autoincrement=False)
    voice_before_id = Column('voice_before_id', BIGINT(), nullable=True, autoincrement=False)
    voice_before_name = Column('voice_before_name', VARCHAR(255), nullable=True, autoincrement=False)
    voice_after_id = Column('voice_after_id', BIGINT(),nullable=True, autoincrement=False)
    voice_after_name = Column('voice_after_name', VARCHAR(255), nullable=True, autoincrement=False)
    mute = Column('mute', BOOLEAN(), nullable=True)
    deaf = Column('deaf', BOOLEAN(), nullable=True)
    stream = Column('stream', BOOLEAN(), nullable=True)
    video = Column('video', BOOLEAN(), nullable=True)
    suppress = Column('suppress', BOOLEAN(), nullable=True)
    time = Column('time', VARCHAR(255), nullable=True, server_default=func.now())

class createConnect():

    def __init__(
        self,
        connect_url: str = "sqlite:///voice.db",
    ):

        self.connect_url = connect_url
        self.Base = declarative_base()

        self.engine = create_engine(
            self.connect_url,
            future=True
        )
        self.metadata_obj = MetaData()
        self.session = Session(self.engine)
        self.conn_sqlalchemy = self.engine.connect()

        
        self.table1 = Table(
            "ActionTable",
            self.metadata_obj,
            Column('id', BIGINT(), autoincrement=True, primary_key=True, nullable=False),
            Column('guild_id', BIGINT(), nullable=False, autoincrement=False),
            Column('guild_name', VARCHAR(255), nullable=False, autoincrement=False),
            Column('user_id', BIGINT(), nullable=False, autoincrement=False),
            Column('user_name', VARCHAR(255), nullable=False, autoincrement=False),
            Column('voice_before_id', BIGINT(), nullable=True, autoincrement=False),
            Column('voice_before_name', VARCHAR(255), nullable=True, autoincrement=False),
            Column('voice_after_id', BIGINT(),nullable=True, autoincrement=False),
            Column('voice_after_name', VARCHAR(255), nullable=True, autoincrement=False),
            Column('mute', BOOLEAN(), nullable=True),
            Column('deaf', BOOLEAN(), nullable=True),
            Column('stream', BOOLEAN(), nullable=True),
            Column('video', BOOLEAN(), nullable=True),
            Column('suppress', BOOLEAN(), nullable=True),
            Column('time', VARCHAR(255), nullable=True, server_default=func.now()),
        )

        if not bool(self.engine.dialect.get_table_names(self.engine.connect())):
            print("create create all tables")
            # self.Base.metadata.create_all(self.engine)
            self.metadata_obj.create_all(self.engine)

    def write_action(self, data: dict, console: bool = False):

        server: dict = data.get("server")  # type: ignore
        user: dict = data.get("user")  # type: ignore
        voice: dict = data.get("voice")  # type: ignore
        before: dict = voice.get("before")  # type: ignore
        after: dict = voice.get("after")  # type: ignore
        state: dict = data.get("state")  # type: ignore

        action = ActionClass(
            guild_id=server.get("id"),
            guild_name=server.get("name"),
            user_id=user.get("id"),
            user_name=user.get("name"),
            voice_before_id=before.get("id"),
            voice_before_name=before.get("name"),
            voice_after_id=after.get("id"),
            voice_after_name=after.get("name"),
            **state,
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.session.add(action)
        self.session.commit()
