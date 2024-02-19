from flask import Flask, request, render_template
from flask_restful import Api, Resource
# from other import summarise
import servicemanager as svm

app = Flask(__name__)
api = Api(app)
sm = svm.ServiceManager()

class JsonFileResource(Resource):
    def get(self, filename=None):
        if filename == "sum_customisation":
            sum_customisation = sm.get_sum_customisation('md.json')
            return {'data': sum_customisation}
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
                print("Summarising")
                print(json_data['text'][0:20])
                print(json_data['customisation'])
                result['data'] = sm.start_summarisation(json_data)
            elif action == "scrape":
                result['data'] = sm.start_scraping(json_data)
            
            return result, 200

        except Exception as e:
            error_message = {"status": "error", "message": str('OH NO: ' + str(e))}
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

@app.route('/home/a')
def index_a():
    return render_template('index.html')

@app.route('/home/c/b')
def index_c_b():
    return render_template('index.html')

@app.route('/home/a/b')
def index_a_b():
    return render_template('index.html')

@app.route('/other/a')
def other_a():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
