from src.discordObserver import DiscordObserver
from src.fetchInfo import get_token

if __name__ == "__main__":
    token_list = get_token()
    token = token_list[2]

    observer = DiscordObserver(
        user_offline=False, 
        voice=True, 
        text=False,
        
        log_write=True,
        write=False,
        console=True,
        connect_url = "sqlite:///observer_data.db",
    )

    observer.run(token)