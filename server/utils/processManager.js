const { name } = require("body-parser");
const child_process = require("child_process");
const { DateTime } = require("luxon");


class ProcessManager {
  constructor(test) {
    this.test = test;
    this.stackChildProcess = new Map([]);
  }

  createBot(token, name, envObj = {}) {
    console.log(' - [ProcessManager]', 'process.createBot')
    var hasToken = [...this.stackChildProcess.values()].find(
      (item) => item.token == token
    );
    var andOfMap = [...this.stackChildProcess.keys()].pop()
    var id = !andOfMap ? 1 : andOfMap + 1
    var file = this.test ? "bot/testFile.js" : "bot/observerDS.js";
    if (!!hasToken) {
      console.log(' - [ProcessManager]', 'process.createBot', 'error: token is in use now')
      return {
        id: null, 
        discription: 'error: token is in use now'
      };
    }
    var anyProcess = child_process.fork(file,{
      env: {
        ...process.env,
        ...envObj,
        DISCORD_TOKEN: `${token}`
      }
    });

    var obj = {
      name: name,
      token: token,
      code: null,
      status: "run",
      discription: "",
      start: DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss"),
      process: anyProcess,
    };

    this.stackChildProcess.set(id, obj);

    anyProcess.on("close", (code, error, signal) => {
      // var prcs = this.stackChildProcess.get(id);
      this.stackChildProcess.set(id, {
        ...obj,
        code: code,
        status: "stoped",
        discription: `${error}`,
        process: anyProcess,
      });
    });
    
    console.log(' - [ProcessManager]', 'process.createBot', 'bot is been created')
    return  {
      id: id, 
      discription: 'OK'
    };
  }

  killProcessById(id) {
    var process = this.stackChildProcess.get(id);

    try {
      
      process?.process.kill();
      console.log(' - [ProcessManager]', 'process.kill')
    } catch (error) {
      console.log(error);
      return false
    }

    setTimeout(()=>{
      this.stackChildProcess.delete(id);
      console.log(' - [ProcessManager]', 'process.delete', this.stackChildProcess )
    }, 1000)

    return true
  }

  killProcessByName(name) {
    var result = [];
    this.stackChildProcess.forEach(
      (item, key)=>{
        if (item.name.indexOf(name) != -1){
          result.push({id: key, ...item})
        }
      }
    )

    if(result.length > 1){
      return result.map(item=>{return {id: item.id, name: item.name}})  
    }
    if(result.length == 0){
      return []
    }
    if(result.length == 1){
      this.killProcessById(result[0].id)
      return true
    }
  }

  status(name = null, hideToken = true) {
    var keys = [...this.stackChildProcess.keys()]
    

    switch (name) {
      case null:
        try {
          return [...this.stackChildProcess.values()].map((item, index) => {
            return {
              id: keys[index],
              
              ...item,
              token: hideToken ? "hide" : item.token,
              process: null,
            };
          });
        } catch (error) {
          console.log(error)
          return [];
        }
      default:
        return [...this.stackChildProcess.values()].map((item, index) => {
          return {
            id: keys[index] ,
            
            ...item,
            token: hideToken ? "hide" : item.token,
            process: null,
          };
        });
        // return {
        //   ...this.stackChildProcess.find((item) => item.name === name),
        //   process: null,
        //   token: !!hideToken ? "hide" : token,
        // };
    }
  }
}

module.exports = { ProcessManager };
