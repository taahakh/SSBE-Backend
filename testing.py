import unittest
from main import app
from database_models import db, User
from summarisationmanager import SummarisationManager
from model_interface import TextType
import servicemanager, model_interface
import os, json

EXAMPLE_TEXT = """
Ancient Egyptian literature was written with the Egyptian language from ancient Egypt's pharaonic period until the end of Roman domination. It represents the oldest corpus of Egyptian literature. Along with Sumerian literature, it is considered the world's earliest literature.[1]

Writing in ancient Egypt—both hieroglyphic and hieratic—first appeared in the late 4th millennium BC during the late phase of predynastic Egypt. By the Old Kingdom (26th century BC to 22nd century BC), literary works included funerary texts, epistles and letters, hymns and poems, and commemorative autobiographical texts recounting the careers of prominent administrative officials. It was not until the early Middle Kingdom (21st century BC to 17th century BC) that a narrative Egyptian literature was created. This was a "media revolution" which, according to Richard B. Parkinson, was the result of the rise of an intellectual class of scribes, new cultural sensibilities about individuality, unprecedented levels of literacy, and mainstream access to written materials.[2] The creation of literature was thus an elite exercise, monopolized by a scribal class attached to government offices and the royal court of the ruling pharaoh. However, there is no full consensus among modern scholars concerning the dependence of ancient Egyptian literature on the sociopolitical order of the royal courts.

Underground Egyptian tombs built in the desert provide possibly the most protective environment for the preservation of papyrus documents. For example, there are many well-preserved Book of the Dead funerary papyri placed in tombs to act as afterlife guides for the souls of the deceased tomb occupants.[24] However, it was only customary during the late Middle Kingdom and first half of the New Kingdom to place non-religious papyri in burial chambers. Thus, the majority of well-preserved literary papyri are dated to this period.[24]
"""

EXAMPLE_HTML = """  
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <div>
        <div>
            <p>
                Ancient Egyptian literature was written with the Egyptian language from ancient Egypt's pharaonic period until the end of Roman domination. It represents the oldest corpus of Egyptian literature. Along with Sumerian literature, it is considered the world's earliest literature.[1]
            </p>
            <p>
                Writing in ancient Egypt—both hieroglyphic and hieratic—first appeared in the late 4th millennium BC during the late phase of predynastic Egypt. By the Old Kingdom (26th century BC to 22nd century BC), literary works included funerary texts, epistles and letters, hymns and poems, and commemorative autobiographical texts recounting the careers of prominent administrative officials. It was not until the early Middle Kingdom (21st century BC to 17th century BC) that a narrative Egyptian literature was created. This was a "media revolution" which, according to Richard B. Parkinson, was the result of the rise of an intellectual class of scribes, new cultural sensibilities about individuality, unprecedented levels of literacy, and mainstream access to written materials.[2] The creation of literature was thus an elite exercise, monopolized by a scribal class attached to government offices and the royal court of the ruling pharaoh. However, there is no full consensus among modern scholars concerning the dependence of ancient Egyptian literature on the sociopolitical order of the royal courts. 
            </p>
            <p>
                Underground Egyptian tombs built in the desert provide possibly the most protective environment for the preservation of papyrus documents. For example, there are many well-preserved Book of the Dead funerary papyri placed in tombs to act as afterlife guides for the souls of the deceased tomb occupants.[24] However, it was only customary during the late Middle Kingdom and first half of the New Kingdom to place non-religious papyri in burial chambers. Thus, the majority of well-preserved literary papyri are dated to this period.[24]
            </p>
        </div>
    </div>
</head>
<body>
    
</body>
</html>


"""

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
    # Tests SummarisationManager: load_resources(self, src_path) -> bool
    # def test_bad_model_list(self):
    #     pass
    
    def test_model_list(self):
        sm = SummarisationManager()
        self.assertIsNotNone(sm.model_list)

        state, md = sm.model_loader('BartLargeCNN')
        self.assertTrue(state)
        self.assertIsNotNone(md)

        state, md = sm.model_loader('SBERT')
        self.assertTrue(state)
        self.assertIsNotNone(md)

        state, md = sm.model_loader('T5MedicalSummarisation')
        self.assertTrue(state)
        self.assertIsNotNone(md)

        state, md = sm.model_loader('fake')
        self.assertFalse(state)
        self.assertIsNone(md)

        state, md = sm.model_loader('')
        self.assertFalse(state)
        self.assertIsNone(md)

    
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

    def get_test_user_api_key(self):
        response = self.app.post('/auth/login', json={"username": "test_user", "password": "test_password"})
        data = response.get_json()
        return data['api_key']
    
    def invalid_request_summarisation_block(self, headers, json=None):
        if json is None:
            response = self.app.post('/servicemanager/summarise', headers=headers)
        else:
            response = self.app.post('/servicemanager/summarise', headers=headers, json=json)
        
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_request_summarisation(self):
        custom_headers = {'Authorization': 'Bearer '+self.get_test_user_api_key(), 'Content-Type': 'application/json'}

        # Test with no data (JSON)
        self.invalid_request_summarisation_block(custom_headers)


        # Test with empty data
        self.invalid_request_summarisation_block(custom_headers, {})

        # Not trying all combinations, just a few. The rest are similar. All will fail if its missing any keys and values
        # just a simple or comparison
        self.invalid_request_summarisation_block(custom_headers, {"text" : ""})

        self.invalid_request_summarisation_block(custom_headers, {"customisation" : ""})

        self.invalid_request_summarisation_block(custom_headers, {"customisation" : {}})

        self.invalid_request_summarisation_block(custom_headers, {"extractedType" : ""})

        # Test with empty everything
        self.invalid_request_summarisation_block(custom_headers, {"text" : "", "customisation" : {}, "extractedType" : ""})

        # Test with empty text
        self.invalid_request_summarisation_block(custom_headers, {"text" : "", "customisation" : {}, "extractedType" : "html"})

        # Test with empty customisation
        self.invalid_request_summarisation_block(custom_headers, {"text" : "test", "customisation" : {}, "extractedType" : "html"})

        # Test with empty extractedType
        self.invalid_request_summarisation_block(custom_headers, {"text" : "test", "customisation" : {}, "extractedType" : ""})


    def test_invalid_request_data_summarisation(self):
        custom_headers = {'Authorization': 'Bearer '+self.get_test_user_api_key(), 'Content-Type': 'application/json'}

        #Test invalid HTML extraction
        self.invalid_request_summarisation_block(custom_headers, {"text" : "not html - missing html tag", "customisation" : {}, "extractedType" : "html"})

        #Test invalid summary length
        self.invalid_request_summarisation_block(custom_headers, {"text" : "test", "customisation" : {"summary-length" : -1}, "extractedType" : "extracted"})
        self.invalid_request_summarisation_block(custom_headers, {"text" : "test", "customisation" : {"summary-length" : 101}, "extractedType" : "extracted"})

        #Test invalid model
        self.invalid_request_summarisation_block(custom_headers, {"text" : "test", "customisation" : {"model" : ""}, "extractedType" : "extracted"})
        self.invalid_request_summarisation_block(custom_headers, {"text" : "test", "customisation" : {"model" : "invalidmodel"}, "extractedType" : "extracted"})
        self.invalid_request_summarisation_block(custom_headers, {"text" : "test", "customisation" : {"model" : "bartlargecnn"}, "extractedType" : "extracted"}) #case sensitive

    def valid_request_summarisation_block(self, json):
        custom_headers = {'Authorization': 'Bearer '+self.get_test_user_api_key(), 'Content-Type': 'application/json'}
        
        response = self.app.post('/servicemanager/summarise', headers=custom_headers, json=json)
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['data'])

    def test_valid_request_summarisation(self):

        # Test with extracted text
        self.valid_request_summarisation_block({"text" : EXAMPLE_TEXT, "customisation" : {"model" : "BartLargeCNN"}, "extractedType" : "extracted"})
        
        # Test with html
        self.valid_request_summarisation_block({"text" : EXAMPLE_HTML, "customisation" : {"model" : "BartLargeCNN"}, "extractedType" : "html"})

        # Test with custom summary length
        self.valid_request_summarisation_block({"text" : EXAMPLE_TEXT, "customisation" : {"model" : "BartLargeCNN", "summary-length" : "50"}, "extractedType" : "extracted"})
    
    def test_clean_escape_char(self):
        sm = servicemanager.ServiceManager()
        self.assertEqual(sm.fix_escape_chars("test\\n"), "test")
        self.assertEqual(sm.fix_escape_chars("test\n"), "test")
        self.assertEqual(sm.fix_escape_chars("test\\t"), "test")
        self.assertEqual(sm.fix_escape_chars("test\t"), "test")
        self.assertEqual(sm.fix_escape_chars("test\\\""), 'test"')

    def test_is_model_abstractive(self):
        sm = SummarisationManager()
        self.assertIsInstance(sm.is_model_abstractive("BartLargeCNN"), model_interface.ModelInterface)
        # self.assertTrue(sm.is_model_abstractive("BartLargeCNN"))
        self.assertIsNone(sm.is_model_abstractive("SBERT"))
        self.assertIsInstance(sm.is_model_abstractive("T5MedicalSummarisation"), model_interface.ModelInterface)

if __name__ == '__main__':
    unittest.main()