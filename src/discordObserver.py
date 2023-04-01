from discord import Status, Client
from .write import  CloneLogger, Checker
from .castomTread import CreateInfiniteLoop
from .fetchInfo import fetch_change_room_log, fetch_change_room_data, fetch_structure_guilds, fetch_structure_guilds_multuTreth


from .dbModule import createConnect

from json import dump
from datetime import datetime

def write_in_file(data, name: str = "",):

    if name == "":
        name = "{:%Y:%m:%d-%H:%M:%S}".format(datetime.now())

    file_name = '{}.json'.format(name)

    f = open(file_name, "a")

    with open(file_name, 'w', encoding='utf8') as file_name:
        dump(data, file_name, ensure_ascii=False)

    f.close()   

    return file_name

class DiscordObserver(Client):
    r"""
        Сreate an observer for any guild if the user is following it

        Parameters
        -----------
        
        user_offline: set user's status online/ofline
        voice: subscribe update voice channels
        text: subscribe update text channels

        write: log entry in file 
        console: log entry in console
        path: path log file

        target_list: list of [id] target guilds
        ignor_list: list of [id] ignor guilds
    """

    def __init__(
            self, 
            user_offline: bool = True,

            voice: bool = False, 
            text: bool = False, 

            db_write: bool = True,

            connect_url: str = "sqlite:///observer_data.db",

            log_write: bool = False,

            write: bool = False, 
            console: bool = False, 
            path:str = "./",

            target_list: list[int] = [], 
            ignor_list: list[int] = [], 
        ):
       
        # self.token = token 
        self.user_offline = user_offline

        self.voice = voice
        self.text = text

        self.db_write = db_write
        self.connect_url = connect_url

        self.log_write = log_write
        
        self.write = write
        self.console = console
        self.path = path

        self.target_list = target_list
        self.ignor_list = ignor_list

        self.on_ready_ = False

        self.client = Client() 
        if self.db_write:
            connect = createConnect(connect_url=self.connect_url)

        @self.client.event
        async def on_ready():
            if self.user_offline:
                await self.client.change_presence(status=Status.invisible)
                await self.client.change_presence(status=Status.offline)

           
            # date_structure = get_all_info_multuTreth(self.client) # type: ignore
            # write_in_file(date_structure)
            # self.on_ready_ = True
            user = f'{self.client.user.name}#{self.client.user.discriminator}' # type: ignore 
            print(f'We have logged in as {user}')

            print("GETTING DATA...")

        


        if self.voice :
            if self.log_write:
                voice_log = CloneLogger(
                        "voice", 
                        path=self.path, 
                        console=self.console, 
                        write=self.write
                    )
            
            @self.client.event
            async def on_voice_state_update(member, before, after):
                if not bool(ignor_list) and not bool(target_list):
                    if self.log_write:
                        voice_log.info(await fetch_change_room_log(member, before, after))
                    if self.db_write:
                        connect.write_action( await fetch_change_room_data(member, before, after))
                    
                elif bool(target_list) and member.guild.id in target_list:
                    if self.log_write:
                        voice_log.info( await fetch_change_room_log(member, before, after))
                    if self.db_write:
                        connect.write_action( await fetch_change_room_data(member, before, after))

                elif bool(ignor_list) and not member.guild.id in ignor_list:
                    if self.log_write:
                        voice_log.info( await fetch_change_room_log(member, before, after))
                    if self.db_write:
                        connect.write_action( await fetch_change_room_data(member, before, after))
            
        if self.text:
            text_log = CloneLogger("text", path=self.path, console=self.console, write=self.write)
            # CreateInfiniteLoop(Checker(text_log).check).start_practice()
            @self.client.event
            async def on_message(message):

                data = {
                    "server": {
                        "id":message.guild.id,
                        "name":message.guild.name,
                    },
                    "user": {
                        "id":message.author.id,
                        "name": message.author.name + "#" + message.author.discriminator,
                    },
                    "text": message.content,
                    "contents": message.attachments
                }

                print(data)

                if not bool(ignor_list) and not bool(target_list):
                    text_log.info( data )
                elif bool(target_list) and message.guild.id in target_list:
                    text_log.info( data )
                elif bool(ignor_list) and not message.guild.id in ignor_list:
                    text_log.info( data )
                

    def run(self, token):
        self.client.run(token)
