const express = require("express");
const bodyParser = require("body-parser");
require("dotenv").config();
const { ProcessManager } = require("./utils/processManager.js");

const app = express();
const PORT = process.env.APIPORT;
var pm = new ProcessManager();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


// const sendPageFn = (req, res, fileName) => {
//   const options = { root: path.join(__dirname + "/pages") };

//   res.sendFile(fileName, options, function (err) {
//     if (err) {
//       console.log(err);
//     } else {
//       console.log("Sent:", fileName);
//     }
//   });
// };

// web interface
// TODO [ ]: create dashboard use svelte
// app.get("/", (req, res) => {
//   sendPageFn(req, res, "index.html");
//   res.render();
// });

// Rest api
app.post("/create", (req, res) => {
  const { token, name, target, ignore } = req.body;

  if (!name) {
    res.status(400).send("No name");
  }
  if (!token) {
    res.status(400).send("No token");
  }

  var envObj = { TARGET: target, IGNORE: ignore };
  var bot = pm.crtBot(token, name, envObj);

  res.send(JSON.stringify(bot));

});

app.post("/kill", (req, res) => {

  const { name, id} = req.body;
  var status = false

  if(!!id){
    var status = pm.killProcessById(id)
  }
  if(!!name){
    var status = pm.killProcessByName(name)
  }

  res.send(JSON.stringify(status))
  
});

app.get("/status", (req, res) => {
  var { hideToken } = req.body;
  hideToken = hideToken ? false : true
  res.send(pm.status());
});

app.listen(PORT,  () => {
  console.log(`server: localhost:${PORT}`);
});
