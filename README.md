# cerbos-todo
TODO API with cerbos permission checks. TODO REST API with create, update, view and delete.


## Start the Cerbos server

```
docker run --rm --name cerbos -d -v $(pwd)/cerbos-bin/policies:/policies -p 3592:3592 pkg.cerbos.dev/containers/cerbos:0.2.1
```

## Start the TODO server

```
python3 main.py
```

## Validate the permissions by make API call to the endpoints

```
curl -X get -H "token: user2SecretToken" http://localhost:5000/todo/5
```
