from discord import Status, Client
from .fetchInfo import fetch_change_room_data
from .dbModule import createConnect


class Observer(Client):
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
        db_write: bool = True,
        connect_url: str = "sqlite:///observer_data.db",
        target_list: list[int] = [],
        ignor_list: list[int] = [],
    ):

        self.user_offline = user_offline
        self.voice = True

        self.db_write = db_write
        self.connect_url = connect_url

        self.target_list = target_list
        self.ignor_list = ignor_list

        self.on_ready_ = False

        self.client = Client()
    
        connect = createConnect(connect_url=self.connect_url)

        @self.client.event
        async def on_ready():
            # type: ignore
            user = f'{self.client.user.name}#{self.client.user.discriminator}'
            print(f'We have logged in as {user}')

            print("GETTING DATA...")

        if self.voice:
            @self.client.event
            async def on_voice_state_update(member, before, after):
                if not bool(ignor_list) and not bool(target_list):
                    connect.write_action(await fetch_change_room_data(member, before, after))

                elif bool(target_list) and member.guild.id in target_list:
                    connect.write_action(await fetch_change_room_data(member, before, after))

                elif bool(ignor_list) and member.guild.id not in ignor_list:
                    connect.write_action(await fetch_change_room_data(member, before, after))

    def run(self, token):

        self.client.run(token)

