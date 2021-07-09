from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from resources import Tokens, TodoItems, Users

import cerbos
import uuid

app = Flask(__name__)
api = Api(app)

CERBOS_URL="http://localhost:3592"

class TODO(Resource):
    @app.route("/todo/<string:id>")
    def get(id):
        if not TODO.__authenticate(request.headers["token"]):
            return {'message': 'API key invalid'}, 401
        
        client = cerbos.Client(host=CERBOS_URL)
        todo_request = cerbos.ResourceInstance(
            attr=TodoItems[id]
        )

        userId = Tokens[request.headers["token"]]
        user = Users[userId]
        principal = cerbos.Principal(
            id=userId,
            roles=[user["role"]],
            attr=user,
        )
        if not TODO.check(client, principal, "view", todo_request):
            return { 'data': 'Not authorized' }, 401
        
        return {'data': id}, 200

    def post(self):
        if not TODO.__authenticate(request.headers['TOKEN']):
            return {'message': 'API key invalid'}, 401
        
        client = cerbos.Client(host=CERBOS_URL)
        todo_request = cerbos.ResourceInstance(
            attr=TodoItems[id]
        )

        userId = Tokens[request.headers["token"]]
        user = Users[userId]
        principal = cerbos.Principal(
            id=userId,
            roles=[user["role"]],
            attr=user,
        )
        if not TODO.check(client, principal, "create", todo_request):
            return { 'data': 'Not authorized' }, 401

        return {'message': 'success'}, 201

    @app.route("/todo/<int:id>", methods = ['PUT'])
    def put(id):
        if not TODO.__authenticate(request.headers['TOKEN']):
            return {'message': 'API key invalid'}, 401
        
        client = cerbos.Client(host=CERBOS_URL)
        todo_request = cerbos.ResourceInstance(
            attr=TodoItems[id]
        )

        userId = Tokens[request.headers["token"]]
        user = Users[userId]
        principal = cerbos.Principal(
            id=userId,
            roles=[user["role"]],
            attr=user,
        )
        if not TODO.check(client, principal, "update", todo_request):
            return { 'data': 'Not authorized' }, 401

        return {'data': id}, 200

    def delete(self):
        if not TODO.__authenticate(request.headers['TOKEN']):
            return {'message': 'API key invalid'}, 401
        
        client = cerbos.Client(host=CERBOS_URL)
        todo_request = cerbos.ResourceInstance(
            attr=TodoItems[id]
        )

        userId = Tokens[request.headers["token"]]
        user = Users[userId]
        principal = cerbos.Principal(
            id=userId,
            roles=[user["role"]],
            attr=user,
        )
        if not TODO.check(client, principal, "delete", todo_request):
            return { 'data': "Not authorized" }, 401

        return {'message': 'success'}, 200
    
    def __authenticate(token):
        if token in Tokens:
            print("true")
            return True
        else:
            print("false")
            return False

    def check(
        client: cerbos.Client,
        principal: cerbos.Principal,
        action: str,
        resource: cerbos.ResourceInstance,
    ):
        # Build the Cerbos request
        request = cerbos.CheckResourceSetRequest(
            request_id=str(uuid.uuid4()),
            actions=[action],
            principal=principal,
            resource=cerbos.ResourceSet(
                kind="todo", instances={resource.attr["id"]: resource}
            ),
        )
        print(request)
        try:
            # Make a Cerbos request
            response = client.check_resource_set(request)

            # Check whether the Cerbos response indicates that this action is allowed
            return response.is_allowed(resource.attr["id"], action)
        except cerbos.ClientException as e:
            print(f"Request failed: {e.msg}")

api.add_resource(TODO, '/todo')

if __name__ == '__main__':
    app.run()
