import json

async def fetch_change_room_data(member, before, after):

    channel_before = before.channel
    channel_after = after.channel
    guild = member.guild
    member_state = None

    voice = {
                "before": str(channel_before), 
                "after": str(channel_after)
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
            "user": {"name": member.name, "id": member.id}, 
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



def get_token(file_name:str = 'token.json'):
    f = open(file_name)
    data = json.load(f)
    list_:list[str] = []

 
    for token in data.get("tokens"):
        list_.append(token.get("token"))   

    f.close()     
    return list_

