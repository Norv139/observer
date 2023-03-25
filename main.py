from src.discordObserver import DiscordObserver
from src.fetchInfo import get_token

if __name__ == "__main__":
    observer = DiscordObserver(voice=True, text=True, write=True, console=True, path="./log")

    token_list = get_token()
    token = token_list[0] # type: ignore
    observer.run("ALKjfkahnsdlkalkscjasbwudsgqwuidjqpwl;fkqa[pevizdcgbvjakwndm[pqwafiahouvj]]")

