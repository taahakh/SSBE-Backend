from flask import Flask, request
from flask_restful import Api, Resource
from other import summarise

app = Flask(__name__)
api = Api(app)

class JsonFileResource(Resource):
    def get(self):
        return {'json': 'this is get mate'}
    
    def post(self):
        try:
            # Assuming the JSON file is in the request body
            json_data = request.get_json()

            # Process the JSON data (you can modify this based on your requirements)
            result = {"status": "success", "message": "JSON file received successfully", "data": summarise(json_data["text"])}

            return result, 200

        except Exception as e:
            error_message = {"status": "error", "message": str('OH NO: ', e)}
            return error_message, 400

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

# Add the resource to the API with the specified endpoint
api.add_resource(JsonFileResource, '/jsonfile')

if __name__ == '__main__':
    app.run(debug=True)
