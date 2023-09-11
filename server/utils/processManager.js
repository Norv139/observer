const { name } = require("body-parser");
const child_process = require("child_process");
const { DateTime } = require("luxon");


class ProcessManager {
  constructor(test) {
    this.test = test;
    this.stackChildProcess = new Map();
  }

  crtBot(token, name, envObj = {}) {
    const hasToken = [...this.stackChildProcess.values()].find(
      (item) => item.token == token
    );

    const andOfMap = [...this.stackChildProcess.keys()].pop()

    var id = !andOfMap ? 1 : andOfMap + 1


    const file = this.test ? "bot/testFile.js" : "bot/observerDS.js";

    if (!!hasToken) {
      return {
        id: undefined, 
        discription: 'error: token is in use now'
      };
    }

    const anyProcess = child_process.fork(file, {
      silent: true,
      detached: true, 
      stdio: 'ignore',
    }, {
      env: {
        ...process.env,
        DISCORD_TOKEN: token,
        ...envObj,
      },
    });

    const obj = {
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
        const prcs = this.stackChildProcess.get(id);
  
        this.stackChildProcess.set(id, {
          ...obj,
          code: code,
          status: "stoped",
          discription: `${error}`,
          process: anyProcess,
        });
      });

    // -=-

    // (code, error, signal) => {
    //   const prcs = this.stackChildProcess.get(id);

    //   this.stackChildProcess.set(id, {
    //     ...obj,
    //     code: code,
    //     status: "stoped",
    //     discription: `${error}`,
    //     process: anyProcess,
    //   });
    // }

    return  {
      id: id, 
      discription: 'OK'
    };
  }

  killProcessById(id) {
    const process = this.stackChildProcess.get(id);

    try {
      process?.process.kill();
    } catch (error) {
      console.log(error);
      return false
    }

    this.stackChildProcess.delete(id);

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
    const keys = [...this.stackChildProcess.keys()]
    

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
