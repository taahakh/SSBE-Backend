from flask import Flask, request, render_template, jsonify, current_app
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
from database_models import db, User
import uuid
# from other import summarise
import servicemanager as svm

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app;
db.init_app(app);
# db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme="Bearer")
api = Api(app)

# with app.app_context():
#     db.create_all()

sm = svm.ServiceManager()

def has_token_user(request):
    if 'Authorization' not in request.headers:
        return False

    auth_header = request.headers['Authorization']
    if not auth_header.startswith('Bearer '):
        return False

    key = auth_header.split(' ')[1]
    user = User.query.filter_by(api_key=key).first()
    return user is not None

@auth.verify_token
def verify_token(token):
    print(token)
    if not token:
        return None
    user = User.query.filter_by(api_key=token).first()
    print(user)
    return user


class LoginResource(Resource):
    def post(self):
        print(User.query.all())
        print(request.headers)
        # print(has_token_user(request))
        # if (has_token_user(request)):
        #     print("Login success - APIKEY: ", request.authorization)
        #     return jsonify({'message': 'Login/Connect Successful!', 'state' : 'GOOD'})
        # else:
        x = request.get_json()
        print(x)
        user = User.query.filter_by(username=x['username']).first()
        
        if user is None:
            print("Login FAILED - User doesn't exist: ")
            return jsonify({'message': 'User does not exist!', 'state' : 'BAD'})

        print("Login success: ", user)
        return jsonify({"message": "Login/Connect Successful!", "api_key" : user.api_key, 'state' : 'GOOD'})


class SignupResource(Resource):
    def post(self):
        x = request.get_json()
        print(x)
        user = User.query.filter_by(username=x['username']).first()
        if user is None:
            key = str(uuid.uuid4())
            user = User(username=x['username'], password=x['password'], api_key=key)
            db.session.add(user)
            db.session.commit()
            return jsonify({"message" : "Signup Successful!", "api_key" : key, 'state' : 'GOOD'})
        else:
            return jsonify({'message' : "User already exists!", 'state' : 'BAD'})

class JsonFileResource(Resource):
    @auth.login_required
    def get(self, filename=None):
        # print(request.headers)
        print(auth.current_user())
        if filename == "sum_customisation":
            sum_customisation = sm.get_sum_customisation('md.json')
            return {'data': sum_customisation}
        return {'json': 'this is get mate'}

class ServiceManagerResource(Resource):
    def get(self, action=None):
        result = {}
        if action == "getsummary":
            finished, data = sm.check_summarisation_stat()
            if finished:
                result['data'] = data['output']
            result['finished'] = finished
        return jsonify(result)
    
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
                print(json_data['extractedType'])
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
api.add_resource(SignupResource, '/auth/signup');
api.add_resource(LoginResource, '/auth/login');

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/home/a')
def index_a():
    return render_template('test.html')

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