const { Client } = require("discord.js-selfbot-v13");
const { DateTime } = require("luxon");
const { exec } = require('node:child_process');
require("dotenv").config();

const { sequelize, ActionTable } = require("../DBconnect/connectPostgreSQL");

// const { and } = require("sequelize");
const token_discord = `${process.env.DISCORD_TOKEN}`;

const target = !!process.env.TARGET ? process.env.TARGET.split(",") : undefined;
const ignore = !!process.env.IGNORE ? process.env.IGNORE.split(",") : undefined;


sequelize.authenticate();
sequelize.sync({ alter: true }).then(() => {}); // Doesn't drop table

console.error("Connection has been established successfully.");

const client = new Client({});

client.on("voiceStateUpdate", async (oldState, newState) => {
  try {
    var globalGuild =
      oldState.channel == null ? newState.channel : oldState.channel;

    const action = {
      guild_id: `${globalGuild.guild.id}`,
      guild_name: `${globalGuild.guild.name}`,
      user_id: `${newState.user.id}`,
      user_name:
        newState.user.discriminator == "0"
          ? `${newState.user.username}`
          : `${newState.user.username}#${newState.user.discriminator}`,
      voice_before_id: oldState.channel == null ? null : oldState.channel.id,
      voice_before_name:
        oldState.channel == null ? null : oldState.channel.name,
      voice_after_id: newState.channel == null ? null : newState.channel.id,
      voice_after_name:
        newState.channel == null ? null : newState.channel.name,
      mute: newState.channel == null ? false : newState.selfMute,
      deaf: newState.channel == null ? false : newState.selfDeaf,
      stream: newState.channel == null ? false : newState.streaming,
      video: newState.channel == null ? false : newState.selfVideo,
      suppress: newState.channel == null ? false : newState.suppress,
      time: DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss"),
    };
    // target != null
    if (!!target && target.indexOf(`${globalGuild.guild.id}`) !== -1) {
      ActionTable.create(action);
    }
    // target == null, ignore != null 
    if (
      !target &&
      !!ignore &&
      ignore.indexOf(`${globalGuild.guild.id}`) == -1
    ) {
      ActionTable.create(action);
    }
    if (!target && !ignore) {
      ActionTable.create(action);
    }
  } catch (error) {
    console.log("Error", error);
  }
});

client.login(`${token_discord}`);
