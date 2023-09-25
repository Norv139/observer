
from src.observer import Observer

from multiprocessing import Process
from flask import Flask, abort, jsonify, request
from flask_restful import Api
from sqlalchemy import URL
import os
# from src.fetchInfo import get_token

APP_PORT = os.getenv('DB_NAME') or 8000
DB_NAME = os.getenv('DB_NAME') or 'cloud_db'
DB_USER = os.getenv('DB_USER') or "admin_cloud"
DB_PASS = os.getenv('DB_PASS') or "admin"
DB_PORT = os.getenv('DB_PORT') or 5432
DB_HOST = os.getenv('DB_HOST') or "localhost"

url = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    port=DB_PORT,
    host=DB_HOST,
)

app = Flask(__name__)
api = Api(app)

class TProcess(object):
    name: str
    token: str
    target: [int | str]
    ignore: [int | str]
    process: object

def anyRunFn(token, target, ignor):
    observer = Observer(
        connect_url=url,
        ignor_list=ignor,
        target_list=target
    )
    observer.run(token)

class ProcessManager(object):
    def __init__(self):

        self.stack = dict({})
        self.stackProcess = dict({})
        self.mapName = dict()
    
    def status(self, id_ = None):  
        print(self.stackProcess)
        if id_ == None:
            return self.stack
        return self.stack.get(id_) 

    def create(self, name = "", token = "", target = [], ignore = []):
        try:
            id_ = len(self.stack) + 1

            if self.mapName.get(name) is not None:
                return {"status": "error", 'dis': "this name is used"}

            try:
                for envItem in self.stack.values():
                    envToken = envItem.get('token')
                    if envToken == token:
                        return {"status": "error", 'dis': "this token is used"} 
            except: 
                return {"status": "error", 'dis': "?"}

            process_ = Process(target=anyRunFn, args=(token, target, ignore, ), name=name)

            process_.exitcode

            process_.start()
        
            self.mapName[name] = id_  # storage of name - id
            self.stackProcess[id_] = process_ # storage with access process
            self.stack[id_] = {  # storage env object 
                'name': name,
                'token': token,
                'target': target,
                'ignore': ignore
            }
            
            return {"status": "ok", 'dis': "bot is created", 'id': id_}
        except:  # noqa: E722
            return {"status": "error", 'dis': "?"}
        
    def delite(self, id_ = None, name = None):

        if id_ != None:
            process_ =  self.stackProcess.get(id_)
        
        if name != None :
            id_ = self.mapName.get(name)
            process_ = self.stackProcess.get(id_)

        # processPid = process_.pid
        # os.kill(processPid, signal.SIGKILL)
        process_.terminate()
        
        if name == None:
            name = self.stack.get(id_)

        del self.stackProcess[id_]
        del self.stack[id_]
        del self.mapName[name]
            
        return {"status": "ok", 'dis': "bot is delited", 'id': id_} 

pm = ProcessManager()

@app.route('/status', methods=['GET'])
def status():
    try: 
        id_ = request.json.get('id')
        status = pm.status(id_=id_)
    except: 
        status = pm.status()
        
    return jsonify({'status': status}), 201

@app.route('/create', methods=['POST'])
def create():

    if 'name' not in request.json or 'token' not in request.json:  # noqa: F821
        abort(400)

    name, token = request.json.get('name'), request.json.get('token')
    target = request.json.get('target') or []
    ignore = request.json.get('ignore') or []

    status = pm.create(name=name, token=token, target=target, ignore=ignore)
    
    return jsonify({'status': status}), 201

@app.route('/delite', methods=['POST'])
def delite():
    id_, name = request.json.get('id'), request.json.get('name')
    
    if id_ != None:
        status = pm.delite(id_=id_)
    elif name != None:
        status = pm.delite(name=name)
    else:
        status = {"status": "error", 'dis': "name or id doesn't exist"}
    
    return jsonify({'status': status}), 201


if __name__ == '__main__':
    app.run(port=APP_PORT)