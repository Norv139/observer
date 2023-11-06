const bigObj = {
  main: [
    process.env.DB_NAME,
    process.env.DB_USER,
    process.env.DB_PASS,
    process.env.DISCORD_TOKEN,
    `TARGET ${process.env.TARGET == undefined ? undefined : process.env.TARGET.split(",")}`,
    `IGNORE ${process.env.IGNORE == undefined ? undefined : process.env.IGNORE.split(",")}`,
  ],
}

console.log(bigObj);
setTimeout(() => {}, 2500000, "");
