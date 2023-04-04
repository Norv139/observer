from src.discordObserver import DiscordObserver
from src.fetchInfo import get_token

if __name__ == "__main__":
    token_list = get_token()
    token = token_list[0]

    observer = DiscordObserver(
        voice=True,
        connect_url = "sqlite:///observer_data.db",
        db_console=True,
        ignor_list=[],
        target_list=[]
    )

    observer.run(token)
