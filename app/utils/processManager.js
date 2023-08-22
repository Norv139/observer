const child_process = require("child_process");
const { DateTime } = require("luxon");

class ProcessManager {
  constructor() {
    this.stackChildProcess = [];
  }

  createBot(token, name, envObj = {}) {
    // code:
    //  0 - ok
    //  1 - name used now
    //  2 - token used now
    //  3 - ?
    try {
      var hasName = this.stackChildProcess.find((obj) => obj.name === name);
      var hasToken = this.stackChildProcess.find((obj) => obj.token === token);

      console.log(hasName, hasToken);

      if (!!hasName) {
        return 1;
      }
      if (!!hasToken) {
        return 2;
      }

      const anyProcess = child_process.fork("bot/index.js", [], {
        env: {
          ...process.env,
          DISCORD_TOKEN: token,
          ...envObj,
        },
      });

      anyProcess.on("close", (code, error) => {
        switch (code) {
          case null:
            break;
          case 1:
            break;
          default:
            try {
              this.stackChildProcess = this.stackChildProcess.map((item) => {
                if (item.name != name) {
                  return item;
                } else {
                  return {
                    ...item,
                    code: code,
                    status: `stoped`,
                    discription: `error: ${error}`,
                  };
                }
              });
            } catch (err) {
              console.log(err);
            }

            console.log(`child_process exit with code: ${code}`);
            break;
        }
      });

      this.stackChildProcess.push({
        name: name,
        token: token,
        start: DateTime.now().toFormat("yyyy-MM-dd HH:mm:ss"),
        code: null,
        status: "run",
        discription: "",
        process: anyProcess,
      });

      return 0;
    } catch (err) {
      console.log(err);
    }
  }

  killProcess(name) {
    var process = this.stackChildProcess.find((item) => item.name === name);

    switch (process) {
      case undefined:
        return process;
      default:
        try {
          process.process.kill();
          this.stackChildProcess = this.stackChildProcess.filter(
            (item) => item.name !== name
          );
          return 0;
        } catch {
          return process;
        }
    }
  }

  status(name = undefined, hideToken = true) {
    switch (name) {
      case undefined:
        try {
          return this.stackChildProcess.map((item) => {
            return {
              ...item,
              process: null,
              token: !!hideToken ? "hide" : token,
            };
          });
        } catch (error) {
          return [];
        }
      default:
        return {
          ...this.stackChildProcess.find((item) => item.name === name),
          process: null,
          token: !!hideToken ? "hide" : token,
        };
    }
  }
}

module.exports = { ProcessManager };
