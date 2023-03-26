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

#### Start like demon:
need yarn 
```
sh start_demon.sh
```

## -- tasks --
- [ ] Add a database to record any state change
	- [ ] Add orm
	- [ ] Add function create standalone/connect database
- [ ] Remove Requirements

- [ ] Wash up and find a job