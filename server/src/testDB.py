from sqlalchemy import MetaData, Table, BIGINT, BOOLEAN, VARCHAR, Column, inspect
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

from sqlalchemy.sql import select

db1 = 'cloud_db'
db2 = 'ather_db'

url = URL.create(
    drivername="postgresql",

    database=db1,
    username="admin_cloud",
    password="admin",

    port=5432,
    host="localhost",
)

engine = create_engine(url, echo=True)

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class ActionTableClass(Base):
    __table__ = Table(
        'ActionTable',
        metadata,
        Column('id', BIGINT(), autoincrement=True, primary_key=True, nullable=False),
        Column('guild_id', BIGINT(), nullable=False, autoincrement=False),
        Column('guild_name', VARCHAR(255), nullable=False, autoincrement=False),
        Column('user_id', BIGINT(), nullable=False, autoincrement=False),
        Column('user_name', VARCHAR(255), nullable=False, autoincrement=False),
        Column('voice_before_id', BIGINT(), nullable=True, autoincrement=False),
        Column('voice_before_name', VARCHAR(255), nullable=True, autoincrement=False),
        Column('voice_after_id', BIGINT(), nullable=True, autoincrement=False),
        Column('voice_after_name', VARCHAR(255), nullable=True, autoincrement=False),
        Column('mute', BOOLEAN(), nullable=True),
        Column('deaf', BOOLEAN(), nullable=True),
        Column('stream', BOOLEAN(), nullable=True),
        Column('video', BOOLEAN(), nullable=True),
        Column('suppress', BOOLEAN(), nullable=True),
        Column('time', VARCHAR(255), nullable=True)
    )
    
    # __tablename__ = 'ActionTable'
    # id = Column('id', BIGINT(), autoincrement=True, primary_key=True, nullable=False)
    # guild_id = Column('guild_id', BIGINT(), nullable=False, autoincrement=False)
    # guild_name = Column('guild_name', VARCHAR(255), nullable=False, autoincrement=False)
    # user_id = Column('user_id', BIGINT(), nullable=False, autoincrement=False)
    # user_name = Column('user_name', VARCHAR(255), nullable=False, autoincrement=False)
    # voice_before_id = Column('voice_before_id', BIGINT(), nullable=True, autoincrement=False)
    # voice_before_name = Column('voice_before_name', VARCHAR(255), nullable=True, autoincrement=False)
    # voice_after_id = Column('voice_after_id', BIGINT(), nullable=True, autoincrement=False)
    # voice_after_name = Column('voice_after_name', VARCHAR(255), nullable=True, autoincrement=False)
    # mute = Column('mute', BOOLEAN(), nullable=True)
    # deaf = Column('deaf', BOOLEAN(), nullable=True)
    # stream = Column('stream', BOOLEAN(), nullable=True)
    # video = Column('video', BOOLEAN(), nullable=True)
    # suppress = Column('suppress', BOOLEAN(), nullable=True)
    # time = Column('time', VARCHAR(255), nullable=True)

inspector = inspect(engine)


if not inspect(engine).has_table('ActionTable'):  # If table don't exist, Create.
    Base.metadata.create_all(engine)
    print('create table')
    
schemas = inspector.get_schema_names()
table = inspector.get_table_names()

try:
    print(schemas, table)
except :
    pass





# +====+====+====+====+====+====+====+====+====+====+

# lestSchemas = []
# for schema in schemas:
    
#     for table_name in inspector.get_table_names(schema=schema):
#         table = []
#         for column in inspector.get_columns(table_name, schema=schema):
#             table.append( column )
#         print(table)
#     print(schema)

# +====+====+====+====+====+====+====+====+====+====+

# def writeDataFromTables ():
#     lestSchemas = []
#     for schema in schemas:
#         for table_name in inspector.get_table_names(schema=schema):
#             table = []
#             for column in inspector.get_columns(table_name, schema=schema):
#                 table.append( "{}".format(column) )
        
#         lestSchemas.append({'name': schema, 'table': table})


#     with open(f'./metaData.json', 'w', encoding='utf-8') as file:
#         json.dump(lestSchemas, file, ensure_ascii=False, indent=4)
            
