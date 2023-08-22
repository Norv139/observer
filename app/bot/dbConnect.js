const { Sequelize, Model, DataTypes } = require("sequelize");
require("dotenv").config();

const database = process.env.DB_NAME || "cloud_db";
const username = process.env.DB_USER || "admin_cloud";
const password = process.env.DB_PASS || "admin";
const dbport = process.env.DB_PORT || 5432;
const DBHOST = process.env.DB_HOST || "localhost";

const tableName = `${process.env.DB_table}` || "ActionTable";

const sequelize = new Sequelize(database, username, password, {
  port: dbport,
  host: DBHOST,
  dialect: "postgres",
});

const ActionTable = sequelize.define(
  tableName,
  {
    id: {
      type: DataTypes.BIGINT,
      autoIncrement: true,
      primaryKey: true,
    },
    guild_id: {
      type: DataTypes.BIGINT,
      allowNull: false,
    },
    guild_name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    user_id: {
      type: DataTypes.BIGINT,
      allowNull: false,
    },
    user_name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    voice_before_id: {
      type: DataTypes.BIGINT,
      allowNull: true,
    },
    voice_before_name: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    voice_after_id: {
      type: DataTypes.BIGINT,
      allowNull: true,
    },
    voice_after_name: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    mute: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
    },
    deaf: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
    },
    stream: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
    },
    video: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
    },
    suppress: {
      type: DataTypes.BOOLEAN,
      allowNull: true,
    },
    time: {
      type: DataTypes.STRING,
      allowNull: true,
    },
  },
  {
    sequelize,
    freezeTableName: true,
    timestamps: false,
  }
);

module.exports = { sequelize, ActionTable };
