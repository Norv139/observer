const express = require("express");
const cors = require('cors')
const bodyParser = require("body-parser");
require("dotenv").config();
const { ProcessManager } = require("./utils/processManager.js");

const app = express();
const PORT = process.env.APIPORT;
var pm = new ProcessManager(
  // true
  );

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cors())

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
  // console.log(req.body)
  const { token, name, target, ignore } = req.body;

  if (!name) {
    res.json({status: "error", discription: "no name"});
  }
  if (!token) {
    res.json({status: "error", discription: "No token"});
  }

  var envObj = { TARGET: target, IGNORE: ignore };
  var bot = pm.createBot(token, name, envObj);
  if (bot.id == null) {
    res.json({status: "error", ...bot});
  } else {
    res.json({status: "ok", ...bot});
  }
  

});

app.post("/kill", (req, res) => {
  const { name, id} = req.body;
  var status = false

  if(!!id){
    status = pm.killProcessById(id)
  }
  if(!!name){
    status = pm.killProcessByName(name)
  }

  if (status == false){
    res.json({status: 'error'})
    console.log(`error ${name} ${id}`)
  }else{
    res.json({status: "ok"})
    console.log(`bot ${name} ${id} is killed`)
  }

  
});

app.get("/status", (req, res) => {
  // console.log(req)
  var { hideToken } = req.body || {hideToken: false};
  
  hideToken = !!hideToken ? false : true

  res.json(pm.status(hideToken=hideToken));
});

app.listen(PORT,  () => {
  console.log(`server: localhost:${PORT}`);
});
