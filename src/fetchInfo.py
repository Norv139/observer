import concurrent.futures
from discord import Guild, Client, Member, VoiceChannel, TextChannel, CategoryChannel
from discord.abc import GuildChannel
import json

async def fetch_change_room_data(member, before, after):

    channel_before = before.channel
    channel_after  = after.channel
    guild = member.guild

    member_name = str(member.name) + "#" + str(member.discriminator)

    def get_obj(channel):
        if (channel) == None:
            return{"name": None, "id": None}
        else:
            return{"name": channel.name, "id": channel.id}
        
    voice = {
            "before": get_obj(channel_before), 
            "after": get_obj(channel_after)
        }
    
    member_state = {
            "mute" : False,
            "deaf" : False,
            "stream": False,
            "video": False,
            "suppress": False,
        }
    
    if str(channel_before) == str(channel_after):
        member_state = {
                "mute" : member.voice.self_mute,
                "deaf" : member.voice.self_deaf,
                "stream": member.voice.self_stream,
                "video": member.voice.self_video,
                "suppress": member.voice.suppress,
        }

    return {
            "server": {"name": guild.name, "id": guild.id}, 
            "user": {"name": member_name, "id": member.id}, 
            "voice": voice,
            "state": member_state
    }

async def fetch_change_room_log(member, before, after):
    channel_before = before.channel
    channel_after = after.channel

    geniral_channel = None

    guild = member.guild
    member_in_room = []


    if channel_after != None:
        all_member = channel_after.members
        geniral_channel = channel_after
    else:
        all_member = channel_before.members
        geniral_channel = channel_before
    
    for member_one in all_member:
        member_in_room.append( str(member_one.name) + "#" + str(member_one.discriminator) )

    def get_state_user(obj):
        if obj == None:
            return None
        value = []
        for kay in obj:
            if kay * obj.get(kay) != "":
                value.append(kay * obj.get(kay))

        return value
    
    member_name = str(member.name) + "#" + str(member.discriminator)

    if str(channel_before) != str(channel_after):
        return( guild.name + ' | '  + "'" +  member_name + "'" + ' : '  + str(channel_before) + " -> " + str(channel_after) + ' | ' + str(member_in_room) )
    
    else:
        member_state = {
            "mute" : member.voice.self_mute,
            "deaf" : member.voice.self_deaf,
            "stream": member.voice.self_stream,
            "video": member.voice.self_video,
            "suppress": member.voice.suppress,
        }
        return( guild.name + ' | '  + "'" +  member_name + "'" + ' | '  + str(channel_after)  + ' | status :' + str(get_state_user(member_state)))

async def fetch_structure_guilds(
        discord_client: Client, 
        list_id: list[int] = [], 
        ignore_null_member: bool = False , 
        text: bool = True, 
        voice: bool = True, 
        category: bool = True   ):

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

async def fetch_structure_guilds_multuTreth(
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

    return all_guilds

def get_token(file_name:str = 'token.json'):
    f = open(file_name)
    data = json.load(f)
    list_:list[str] = []

 
    for token in data.get("tokens"):
        list_.append(token.get("token"))   

    f.close()     
    return list_

