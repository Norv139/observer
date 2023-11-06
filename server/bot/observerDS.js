const { Client } = require("discord.js-selfbot-v13");
const { DateTime } = require("luxon");
var lodash_ = require('lodash');
const { sequelize, ActionTable } = require("../DBconnect/connectPostgreSQL");

// const { and } = require("sequelize");

const token_discord = process.env.DISCORD_TOKEN;

// const target = !!process.env.TARGET ? process.env.TARGET.split(",") : [];
// const ignore = !!process.env.IGNORE ? process.env.IGNORE.split(",") : [];

// console.log(" - [observerBot] ", 'target', target, 'ignore', ignore)

sequelize.authenticate();
sequelize.sync({ alter: true }).then(() => {}); // Doesn't drop table

console.log(" - [observerBot] Connection has been established successfully.");
// console.log('obsereverDS', token_discord, process.env)

const client = new Client({});

function deepDiff(a,b){
  return lodash_.reduce(a, function(result, value, key) {
    return lodash_.isEqual(value, b[key]) ?
        result : result.concat({'key': key, 'value': value});
  }, [])
}

client.on("voiceStateUpdate", async (oldState, newState) => {
  try {
    
    var globalGuild = (oldState.channel == null) ? newState.channel : oldState.channel

    const action = {
        guild_id: `${globalGuild.guild.id}`,
        guild_name: `${globalGuild.guild.name}`,
        user_id: `${newState.user.id}`,
        user_name:
        newState.user.discriminator == "0"
          ? `${newState.user.username}`
          : `${newState.user.username}#${newState.user.discriminator}`,
        voice_before_id: (oldState.channel == null)? null : oldState.channel.id,
        voice_before_name: (oldState.channel == null)? null : oldState.channel.name,
        voice_after_id: (newState.channel == null)? null : newState.channel.id,
        voice_after_name: (newState.channel == null)? null : newState.channel.name,
        mute: (newState.channel == null)? false : newState.selfMute,
        deaf: (newState.channel == null)? false : newState.selfDeaf,
        stream: (newState.channel == null)? false : newState.streaming,
        video: (newState.channel == null)? false : newState.selfVideo,
        suppress: (newState.channel == null)? false : newState.suppress,
        time: DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss")
    }

    ActionTable.create(action);

  } catch (error) {
    console.log(globalGuild, newState.channel == null, oldState.channel == null);
    console.log('oldState newState', deepDiff(oldState, newState))
    console.log('newState oldState', deepDiff(newState, oldState))
  }
});

client.login(`${token_discord}`);
