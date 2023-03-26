# observer
 
## discription
```
This is a self-bot for discord that records all actions in voice and text channels on servers
```

## -- quick start --

### step 1:

#### Install requirements:

```
python3 -m pip install -r req.txt
```
### step 2:

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

### step 3:

#### Start in console:
```
python3 main.py
```

#### Start like demon:
```
yarn global add pm2
pm2 start 
```

## -- tasks --
- [ ] Add a database to record any state change
	- [ ] Add orm
	- [ ] Add function create standalone/connect database
- [ ] Remove Requirements

- [ ] Wash up and find a job