const {
  Worker
, isMainThread
, parentPort
} = require('node:worker_threads');

console.log('run subT')

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

// console.log(bigObj);

parentPort.on('message', (bigObj) => {                          // принимаем ID вместе с сообщением
  parentPort.postMessage({                                          // передаем ID вместе с результатом
    bigObj
  });
});

setTimeout(() => {}, 2500000, "");
