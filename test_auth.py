import unittest
from main import app
from database_models import db, User
from other import SummarisationManager
from model_interface import TextType
import os, json

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.user = User(username='test_user', password='test_password', api_key='TOKEN')
        with app.app_context():
            # db.create_all()
            db.session.add(self.user)
            db.session.commit()
    
    def tearDown(self):
        with app.app_context():
            db.session.delete(self.user)
            db.session.commit()

    def req_error_block(self, response):
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['state'], 'BAD')
    
    def test_login_route(self):
        response = self.app.post('/auth/login', json={"username": "test_user", "password": "test_password"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['state'], 'GOOD')
        self.assertIsNotNone(data['api_key'])
    
    def test_bad_login_route(self):

        # Test with no data (JSON)
        # fails on line 58, x=request.get_json()
        self.req_error_block(self.app.post('/auth/login'))

        # Test with empty data
        self.req_error_block(self.app.post('/auth/login', json={"" : ""}))

        # Test with empty username
        self.req_error_block(self.app.post('/auth/login', json={"username" : "", "password" : "test_password"}))

        # Test with empty password
        self.req_error_block(self.app.post('/auth/login', json={"username" : "test_user", "password" : ""}))

        # Test with non-existent user
        self.req_error_block(self.app.post('/auth/login', json={"username" : "doesntexist", "password" : ""}))

        # Test with no username and missing password entry
        self.req_error_block(self.app.post('/auth/login', json={"username" : ""}))

        # Test with no password and missing username entry
        self.req_error_block(self.app.post('/auth/login', json={"password" : ""}))

    
    def test_signup_route(self):
        # create a new user
        with app.app_context():
            response = self.app.post('/auth/signup', json={"username": "test_userA", "password": "test_passwordA"})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['state'], 'GOOD')
            self.assertIsNotNone(data['api_key'])
        
            # delete the user
            user = User.query.filter_by(username='test_userA').first()
            db.session.delete(user)
            db.session.commit()
    
    def test_bad_signup_route(self):
        # Test with no data (JSON)
        self.req_error_block(self.app.post('/auth/signup'))

        # Test with empty data
        self.req_error_block(self.app.post('/auth/signup', json={"" : ""}))
        
        # Test with existing user
        self.req_error_block(self.app.post('/auth/signup', json={"test" : "test"}))

        # Test with empty username
        self.req_error_block(self.app.post('/auth/signup', json={"username" : "", "password" : "test_password"}))

        # Test with empty password
        self.req_error_block(self.app.post('/auth/signup', json={"username" : "test_user", "password" : ""}))

        # Test with existing user
        self.req_error_block(self.app.post('/auth/signup', json={"username" : "test_user", "password" : "test_password"}))

        # Test with no username and missing password entry
        self.req_error_block(self.app.post('/auth/signup', json={"username" : ""}))

        # Test with no password and missing username entry
        self.req_error_block(self.app.post('/auth/signup', json={"password" : ""}))
    
    def test_unauthorised_sumcustomisationn_route(self):
        print("HERE")
        response = self.app.get('/jsonfile/sum_customisation')
        data = response.get_json()
        self.assertEqual(response.status_code, 401)

    def test_unauthorised_summarise_route(self):
        print("HERE2")
        response = self.app.post('/servicemanager/summarise')
        print(response)
        data = response.get_json()
        print(data)
        self.assertEqual(response.status_code, 401)

    # Must have bartlargecnn, sbert, t5medicalsummarisation in model list WITH THE DEFAULT CONFIGURATION
    def test_jsonfile_route(self):
        user_response = self.app.post('/auth/login', json={"username": "test_user", "password": "test_password"})
        user_data = user_response.get_json()
        self.assertEqual(user_response.status_code, 200)
        self.assertIsNotNone(user_data['api_key'])

        custom_headers = {'Authorization': 'Bearer '+user_data['api_key'], 'Content-Type': 'application/json'}
        response = self.app.get('/jsonfile/sum_customisation', headers=custom_headers)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data)
        self.assertEqual(len(data['data']), 3)
        # self.assertIsNotNone(data['data']['BartLargeCNN'])
        # self.assertIsNotNone(data['data']['SBERT'])
        # self.assertIsNotNone(data['data']['T5MedicalSummarisation'])
    
    # No test needed, program will terminate given the set conditions within the function
    # def test_bad_model_list(self):
    #     pass
    
    def test_nondefault_model_list(self):
        with open('model_list_TEST.txt', 'w') as file:
            file.write('bartlargecnn\n')
        
        sm = SummarisationManager('model_list_TEST.txt')
        self.assertIsNotNone(sm.model_list)
        self.assertIsNotNone(sm.model_list['BartLargeCNN'])
        
        ml = sm.model_list['BartLargeCNN']
        
        self.assertEqual(ml.model_name, 'BartLargeCNN')
        self.assertEqual(ml.minimum_summary_length, 60)
        self.assertEqual(ml.maximum_summary_length, 512)
        self.assertEqual(ml.summary_type.value, 'Abstractive')
        self.assertEqual(ml.text_type, [TextType.GENERAL, TextType.NEWS, TextType.FINANCIAL, TextType.MEDICAL, TextType.SCIENTIFIC])

        os.remove('model_list_TEST.txt')
    
    def test_check_model_desciption_json_creation(self):
        with open('model_list_TEST.txt', 'w') as file:
            file.write('bartlargecnn\n')
        
        sm = SummarisationManager('model_list_TEST.txt', 'md_TEST.json')

        with open('md_TEST.json', 'r') as file:
            data = json.load(file)
            self.assertIsNotNone(data)
            self.assertEqual(len(data), 1)
            
            md = data[0]
            self.assertIsNotNone(md['model-name'])
            self.assertIsNotNone(md['text-type'])
            self.assertIsNotNone(md['summary-type'])
            self.assertIsNotNone(md['description'])
            self.assertIsNotNone(md['summary-length'])
            self.assertIsNotNone(md['summary-length']['min'])
            self.assertIsNotNone(md['summary-length']['max'])

            self.assertEqual(md['model-name'], 'BartLargeCNN')
            self.assertEqual(md['text-type'], ['General', 'News', 'News', 'Medical', 'Scientific'])
            self.assertEqual(md['summary-type'], 'ab')
            self.assertEqual(md['description'], 'Good for all types of text')
            self.assertEqual(md['summary-length']['min'], 60)
            self.assertEqual(md['summary-length']['max'], 512)
        
        os.remove('model_list_TEST.txt')
        os.remove('md_TEST.json')


if __name__ == '__main__':
    unittest.main()