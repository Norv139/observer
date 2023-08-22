const path = require("path");
var express = require("express");
const bodyParser = require("body-parser");

const { ProcessManager } = require("./utils/processManager");
require("dotenv").config();

const app = express();
const PORT = process.env.APIPORT;
var pm = new ProcessManager();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const sendPageFn = (req, res, fileName) => {
  const options = { root: path.join(__dirname + "/pages") };

  res.sendFile(fileName, options, function (err) {
    if (err) {
      next(err);
    } else {
      console.log("Sent:", fileName);
    }
  });
};

// web interface
// TODO [ ]: create dashboard use svelte
app.get("/", (req, res) => {
  sendPageFn(req, res, "index.html");
  res.render();
});

// Rest api
app.post("/create", (req, res) => {
  const { token, name } = req.body;

  if (!name) {
    res.status(400).send("No name");
  }
  if (!token) {
    res.status(400).send("No token");
  }

  var bot = pm.createBot(token, name);

  switch (bot) {
    case 0:
      res.send("OK");
      break;
    case 1:
      res.status(400).send("Name is used");
      break;
    case 2:
      res.status(400).send("Token is used");
      break;
    default:
      res.status(400).send(bot);
      break;
  }
});

app.post("/kill", (req, res) => {
  const data = req.body;
  const name = data["name"];

  var status = pm.killProcess(name);

  switch (status) {
    case undefined:
      res.send("Bot is not exist");
      break;
    default:
      try {
        res.send("Bot is killed");
      } catch (err) {
        res.send(`Error: ${err}`);
      }
      break;
  }
});

app.get("/status", (req, res) => {
  res.send(pm.status());
});

app.listen(PORT, function () {
  console.log(`server: localhost:${PORT}`);
});
