from discord import Status, Client
from .write import  CloneLogger, Checker
from .castopTread import CreateInfiniteLoop
from .fetchInfo import fetch_change_room_log
from .getAllChannel import get_all_info, get_all_info_multuTreth

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

            write: bool = False, 
            console: bool = False, 
            path:str = "./",

            target_list: list[int] = [], 
            ignor_list: list[int] = [], 
        ):
       
        # self.token = token 
        self.path = path
        self.write = write
        self.console = console

        self.target_list = target_list
        self.ignor_list = ignor_list

        self.on_ready_ = False

        self.client = Client() 

        @self.client.event
        async def on_ready():
            if user_offline:
                await self.client.change_presence(status=Status.invisible)
                await self.client.change_presence(status=Status.offline)
  
            self.on_ready_ = True
            user = f'{self.client.user.name}#{self.client.user.discriminator}' # type: ignore 
            print(f'We have logged in as {user}')
        
        if voice:
            voice_log = CloneLogger("voice", path=self.path, console=self.console, write=self.write)
            voice_checker = Checker(voice_log)
            CreateInfiniteLoop(voice_checker.check).start_practice()

            @self.client.event
            async def on_voice_state_update(member, before, after):
                if not bool(ignor_list) and not bool(target_list):
                    date = await fetch_change_room_log(member, before, after)
                    voice_log.info(date)
                elif bool(target_list) and member.guild.id in target_list:
                    date = await fetch_change_room_log(member, before, after)
                    voice_log.info(date)
                elif bool(ignor_list) and not member.guild.id in ignor_list:
                    date = await fetch_change_room_log(member, before, after)
                    voice_log.info(date)
                
            
        if text:
            text_log = CloneLogger("text", path=self.path, console=self.console, write=self.write)
            text_checker = Checker(text_log)
            CreateInfiniteLoop(text_checker.check).start_practice()

            @self.client.event
            async def on_message(message):
                if not bool(ignor_list) and not bool(target_list):
                    text_log.info( f'''{message.guild.name} | {message.channel.name} | {message.author.name} | {message.content}''' )
                elif bool(target_list) and message.guild.id in target_list:
                    text_log.info( f'''{message.guild.name} | {message.channel.name} | {message.author.name} | {message.content}''' )
                elif bool(ignor_list) and not message.guild.id in ignor_list:
                    text_log.info( f'''{message.guild.name} | {message.channel.name} | {message.author.name} | {message.content}''' )
                

    def get_structure_all_guild(self, ignore_null_member, voice, text, category):

        date_ = get_all_info_multuTreth(
            discord_client=self.client, 
            ignore_null_member=ignore_null_member, 
            voice=voice,
            text=text, 
            category=category
        )
        
        return date_

    def run(self, token):
        self.client.run(token)
