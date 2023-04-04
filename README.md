# observer
 
## discription
```
This is a self-bot for discord that records all actions in voice and text channels on servers
```

## -- quick start --

### step 1:

#### OR write token in token.json file:
```
{
	
	"tokens": [
		
		{"name": "", "token": "token"}
		
	]

}
```

#### OR write the token in the main.py file:
```
...
observer.run(token)
...
```

### step 2:

#### Start in console:
```
sh start.sh
```
or
```
pip3 install discord.py==1.7.3
pip3 install discord.py-self==1.9.2
```

#### Start like demon:
need yarn 
```
sh start_demon.sh
```

## -- tasks --
- [ ] Add a database to record any state change
	- [X] Add orm
	- [X] Add function create standalone/connect database
	- [ ] Add tables relationship
- [ ] do standalone application without requirements
- [ ] do interface