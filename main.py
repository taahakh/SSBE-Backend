from flask import Flask, request, render_template
from flask_restful import Api, Resource
# from other import summarise
import servicemanager as svm

app = Flask(__name__)
api = Api(app)
sm = svm.ServiceManager()

class JsonFileResource(Resource):
    def get(self, filename=None):
        return {'json': 'this is get mate'}

class ServiceManagerResource(Resource):
    def get(self, action=None):
        return {'json': 'this is get mate'}
    
    def post(self, action=None):
        try:
            # Assuming the JSON file is in the request body
            json_data = request.get_json()
            # print(json_data)

            result = {"status" : "success"}
            if action == 'summarise':
                result['data'] = sm.start_summarisation(json_data)
            elif action == "scrape":
                result['data'] = sm.start_scraping(json_data)
            
            return result, 200

        except Exception as e:
            error_message = {"status": "error", "message": str('OH NO: ', e)}
            return error_message, 400

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
api.add_resource(ServiceManagerResource, '/servicemanager/<action>')
api.add_resource(JsonFileResource, '/jsonfile', '/jsonfile/<filename>')

@app.route('/home')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
