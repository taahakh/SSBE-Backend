# main.py is the main entry point for the Flask web application.
# It initialises the Flask app, the RESTful API, the database, and the Service Manager.
# It also contains the resource endpoints for user authentication, user signup, JSON file operations, and the summarisation pipeline

from flask import Flask, request, render_template, jsonify, current_app
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
from database_models import db, User
import uuid
import servicemanager as svm

# Initialising the Flask app
app = Flask(__name__)
CORS(app) # Allow CORS for all routes, not needed for extension
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db' # Database location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable tracking modifications

# Initialising the database
db.app = app;
db.init_app(app);

# Initialising the HTTP Token Authentication
auth = HTTPTokenAuth(scheme="Bearer")

# Initialising the RESTful API
api = Api(app)

# Creating the database
# db = SQLAlchemy(app)
# with app.app_context():
#     db.create_all()

# Initialising the Service Manager
sm = svm.ServiceManager()

def has_token_user(request):
    """
    Check if request contains a valid token for a user.

    Args:
        request: Flask request object.

    Returns:
        bool: True if request contains a valid token for a user, False otherwise.
    """
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
    """
    Verify the authenticity of a token.

    Args:
        token (str): Token to be verified.

    Returns:
        User: User object if token is valid, None otherwise.
    """
    if not token or token == 'null' or token == 'undefined':
        return None
    user = User.query.filter_by(api_key=token).first()
    if user is None:
        return None
    return user

# Resource Endpoint for user authentication
class LoginResource(Resource):
    def post(self):

        x = request.get_json(silent=True)

        # Check if the request contains JSON data
        if x is None or 'username' not in x or 'password' not in x:
            return jsonify({'message' : 'Invalid request!', 'state' : 'BAD'})

        # Retrieve the user from the database if it exists
        user = User.query.filter_by(username=x['username']).first()
        
        # Check if the user exists
        if user is None:
            return jsonify({'message': 'User does not exist!', 'state' : 'BAD'})

        # Check if the password is correct
        if user.password != x['password']:
            return jsonify({'message': 'Password incorrect!', 'state' : 'BAD'})

        return jsonify({"message": "Login/Connect Successful!", "api_key" : user.api_key, 'state' : 'GOOD'})

# Resource Endpoint for user signup
class SignupResource(Resource):
    def post(self):
        x = request.get_json(silent=True)

        # Check if the request contains JSON data
        if x is None or 'username' not in x or 'password' not in x:
            return jsonify({'message' : 'Invalid request!', 'state' : 'BAD'})
        
        # Check if the username and password are valid
        if len(x['username']) == 0 or len(x['password']) == 0:
            return jsonify({'message' : 'Invalid request, bad username or password!', 'state' : 'BAD'})

        # Check if the user already exists    
        user = User.query.filter_by(username=x['username']).first()
        if user is None:
            # Generate a unique API key
            key = str(uuid.uuid4())
            # Create a new user
            user = User(username=x['username'], password=x['password'], api_key=key)
            # Add the user to the database
            db.session.add(user)
            db.session.commit()
            return jsonify({"message" : "Signup Successful!", "api_key" : key, 'state' : 'GOOD'})
        else:
            return jsonify({'message' : "User already exists!", 'state' : 'BAD'})

# Resource Endpoint for JSON file operations
# This is used to get the summarisation customisation JSON file
class JsonFileResource(Resource):
    @auth.login_required
    def get(self, filename=None):
        if filename == "sum_customisation":
            sum_customisation = sm.get_sum_customisation('md.json')
            return {'data': sum_customisation}
        return {'json': 'this is get mate'}
# SORT THE RETURN ABOVE

# Resource Endpoint for the summarisation pipeline
class ServiceManagerResource(Resource):
    @auth.login_required
    def post(self, action=None):
        try:
            
            # Check if the request contains JSON data
            json_data = request.get_json(silent=True)

            if json_data is None:
                return {"status": "error", "message": "Invalid request - no JSON data found"}, 400

            result = {"status" : "success"}

            # ENDPOINT for starting summarisation
            if action == 'summarise':

                # Check if the request json is valid
                if 'text' not in json_data or 'customisation' not in json_data or 'extractedType' not in json_data:
                    return {"status": "error", "message": "Invalid request - missing one or more key entries [key, customisation, extractedType]"}, 400

                if json_data['text'] == "" or type(json_data['customisation']) != dict or json_data['extractedType'] == "":
                    return {"status": "error", "message": "Invalid request - one or more key value entries are empty [key, customisation, extractedType]"}, 400

                # Start summarisation
                state, output = sm.start_summarisation(json_data)

                # Check if summarisation was successful
                if not state:
                    return {"status": "error", "message": "Summarisation failed"}, 400
                
                result['data'] = output
            
            return result, 200

        except Exception as e:
            error_message = {"status": "error", "message": str('Message: : ' + str(e))}
            return error_message, 400
        

# Add the resources to the API
api.add_resource(ServiceManagerResource, '/servicemanager/<action>')
api.add_resource(JsonFileResource, '/jsonfile', '/jsonfile/<filename>')
api.add_resource(SignupResource, '/auth/signup');
api.add_resource(LoginResource, '/auth/login');


# --- Test routes ---

# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

# api.add_resource(HelloWorld, '/')

# @app.route('/home')
# def index():
#     return render_template('index.html')

# @app.route('/home/a')
# def index_a():
#     return render_template('test.html')

# @app.route('/home/c/b')
# def index_c_b():
#     return render_template('index.html')

# @app.route('/home/a/b')
# def index_a_b():
#     return render_template('index.html')

# @app.route('/other/a')
# def other_a():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)