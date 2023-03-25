import concurrent.futures
from discord import Guild, Client, Member, VoiceChannel, TextChannel, CategoryChannel
from discord.abc import GuildChannel

async def get_all_info(discord_client: Client, list_id: list[int] = [], ignore_null_member: bool = False , text: bool = True, voice: bool = True, category: bool = True):

    all_guilds = []

    for guild in discord_client.guilds.copy():



        if len(list_id) != 0:
            if guild.id in list_id:
                pass
            else:    
                continue

        voice_channel = []
        text_channel =[]
        category_channel = []

        for channel in guild.channels.copy():

            all_members = []

            all_roles = []

            for role in channel.changed_roles.copy():
                all_roles.append(str(role))

            try:
                for member in channel.members.copy():
                    all_members.append(
                        {
                            "id": member.id,
                            "name": member.name  + "#" + member.discriminator
                        }
                    )
                
                obj = {
                        "id": channel.id,
                        "name": channel.name,
                        "type": str(channel.type),
                        "members": all_members,
                        "role": all_roles
                    }

                if str(channel.type) == "voice" and voice == True:

                    if ignore_null_member != False:
                        if len(all_members) != 0:
                            voice_channel.append(obj)
                        else:
                            pass
                    else:
                        voice_channel.append(obj)

                elif str(channel.type) == "text" and text == True:
                    text_channel.append(obj)
                else:
                    pass
            except:
                if category == True:
                    category_channel.append({
                            "id": channel.id,
                            "name": channel.name,
                            "type": str(channel.type)
                        })
                else: 
                    pass
        
        all_guilds.append(
            {   
                "id": guild.id,
                "name": guild.name,
                "voice": voice_channel,
                "text": text_channel,
                "category": category_channel
            }
        )
    
    return all_guilds

def get_all_info_multuTreth(
        discord_client: Client, 
        list_id: list[int] = [], 
        ignore_null_member: bool = False, 
        text: bool = True, 
        voice: bool = True, 
        category: bool = True):
    
    def get_info_from_guild(    
            guild: Guild, 
            returnList: list[object], 
            list_id: list[int] = [], 
            ignore_null_member: bool = False, 
            text: bool = True, 
            voice: bool = True, 
            category: bool = True
        ):

        if len(list_id) != 0:
            if guild.id in list_id:
                pass
            else:    
                return

        voice_channel = []
        text_channel =[]
        category_channel = []

        for channel in guild.channels.copy():
            channel: TextChannel | VoiceChannel | CategoryChannel

            all_members = []

            all_roles = []

            for role in channel.changed_roles.copy():
                all_roles.append(str(role))

            try:
                for member in channel.members.copy(): # type: ignore

                    all_members.append(
                        {
                            "id": member.id,
                            "name": member.name  + "#" + member.discriminator
                        }
                    )
                
                obj = {
                        "id": channel.id,
                        "name": channel.name,
                        "type": str(channel.type),
                        "members": all_members,
                        "role": all_roles
                    }

                if str(channel.type) == "voice" and voice == True:
                    if ignore_null_member != False:
                        if len(all_members) != 0:
                            voice_channel.append(obj)
                        else:
                            pass
                    else:
                        voice_channel.append(obj)

                elif str(channel.type) == "text" and text == True:
                    text_channel.append(obj)
                else:
                    pass
            except:
                if category == True:
                    category_channel.append({
                            "id": channel.id,
                            "name": channel.name,
                            "type": str(channel.type)
                        })
                else: 
                    pass
            
        
        # print(guild.id)

        returnList.append(
            {   
                "id": guild.id,
                "name": guild.name,
                "voice": voice_channel,
                "text": text_channel,
                "category": category_channel
            }
        )
        

        return returnList

    all_guilds = []
    pool = concurrent.futures.ThreadPoolExecutor()

    for guild in discord_client.guilds.copy():
        guild: Guild
        
        pool.submit(
            get_info_from_guild(
                guild = guild, 
                returnList= all_guilds,
                list_id = list_id, 
                ignore_null_member = ignore_null_member, 
                text = text, 
                voice = voice, 
                category = category) # type: ignore
            )

    pool.shutdown()

    print(all_guilds)

    return all_guilds
            