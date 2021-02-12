import unittest
from flask import url_for
from webapp.db_models import User
from webapp.match import get_matching
from webapp import db
from webapp.db_models import Advertisement
from datetime import date
from webapp.util import get_keywords,is_email,get_business_keywords, get_keyword_from_db,get_interest_from_db,get_interests,get_keywords

from run import app

class BlackBoxTest(unittest.TestCase):
#    def test_home(self):
#        # user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#        tester = app.test_client(self)
#        response = tester.get('/home', content_type='html/text')
#        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data, b'Hello World!')
#
#    def test_login(self):
#        # user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#        tester = app.test_client(self)
#        response = tester.get('/login', content_type='html/text')
#        self.assertEqual(response.status_code, 200)
#        # self.assertEqual(response.data, b'Hello World!')


#    def test_users_can_login(self):
#        client = app.test_client(self)
#        response = client.post('/login',
#                                    data={"email":"ertugrulsmz","password":"ertugrulsmz","submit":"Login"},
#                               follow_redirects=True
#                               )
#
#        # print(response.data)
#        self.assertFalse(b'Login Unsuccessful' in response.data)
#        self.assertEqual(response.status_code, 200)
#
#    def test_users_cant_login(self):
#        client = app.test_client(self)
#        response = client.post('/login',
#                                    data={"email":"ertugrulsmz","password":"ertugrulsmz1","submit":"Login"},
#                               follow_redirects=True
#                               )
#
#        # print(response.data)
#        self.assertTrue(b'Login Unsuccessful' in response.data)
#        self.assertEqual(response.status_code, 200)


#    def test_users_can_register(self):
#        client = app.test_client(self)
#        response = client.post('/register',
#                                    data={
#                                        "username":"deneme1",
#                                        "email":"deneme1@gmail.com",
#                                        "password":"deneme1",
#                                        "confirm_password":"deneme1",
#                                        "submit":"Sign Up"},
#                               follow_redirects=True
#                               )
#
#
#        # print(response.data)
#        self.assertTrue(b'Account created for deneme1' in response.data)
#        self.assertEqual(response.status_code, 200)



#    def test_users_cant_register(self):
#        client = app.test_client(self)
#        response = client.post('/register',
#                                    data={
#                                        "username":"deneme1",
#                                        "email":"deneme1@gmail.com",
#                                        "password":"deneme1",
#                                        "confirm_password":"deneme",
#                                        "submit":"Sign Up"},
#                               follow_redirects=True
#                               )
#
#
#        # print(response.data)
#        self.assertTrue(b'Field must be equal to password.' in response.data)
#        self.assertEqual(response.status_code, 200)

#    def test_users_cant_register_for_exist_username(self):
#        client = app.test_client(self)
#        response = client.post('/register',
#                                    data={
#                                        "username":"bucak",
#                                        "email":"deneme1@gmail.com",
#                                        "password":"deneme1",
#                                        "confirm_password":"deneme1",
#                                        "submit":"Sign Up"},
#                               follow_redirects=True
#                               )
#
#
#        # print(response.data)
#        self.assertTrue(b'That username is taken. Please choose a different one.' in response.data)
#        self.assertEqual(response.status_code, 200)


#    def test_users_can_register(self):
#        client = app.test_client(self)
#        response = client.post('/register',
#                                    data={
#                                        "username":"deneme2",
#                                        "email":"deneme2@gmail.com",
#                                        "password":"deneme2",
#                                        "confirm_password":"deneme2",
#                                        "submit":"Sign Up"},
#                               follow_redirects=True
#                               )
#
#        response = client.post('/login',
#                                    data={"email":"deneme2","password":"deneme2","submit":"Login"},
#                               follow_redirects=True
#                               )
#
#        response = client.post('/create_profile_student',
#                                    data={
#                                        "name":"deneme2",
#                                        "university":"deneme2@gmail.com",
#                                        "class_level":"1",
#                                        "gpa":"2",
#                                        "submit":"Create"},
#                               follow_redirects=True
#                               )
#
#        print(response.data)
#        self.assertTrue(b'Business Keywords' in response.data)
#        self.assertEqual(response.status_code, 200)


#    def test_users_can_logout(self):
#        client = app.test_client(self)
#        response = client.post('/login',
#                                    data={"email":"ertugrulsmz","password":"ertugrulsmz","submit":"Login"},
#                               follow_redirects=True
#                               )
#
#        response = client.get('/logout')
#        print(response.data)
#        self.assertEqual(response.status_code, 302)


#        def test_users_can_create_job_advertisement(self):
#            client = app.test_client(self)
#            response = client.post('/login',
#                                        data={"email":"ecorp","password":"ecorp","submit":"Login"},
#                                   follow_redirects=True
#                                   )
#
#            response = client.post('/create_advertisement',
#                                   data={"title": "test job", "description": "ecorp", "submit": "Login"},
#                                   follow_redirects=True
#                                   )
#
#            # response = client.get('/logout')
#            print(response.data)
#            self.assertEqual(response.status_code, 200)
#            self.assertTrue(b'Recently Used' in response.data)


# TODO

#        def test_admin_users_can_delete_job_advertisement(self):
#            client = app.test_client(self)
#            response = client.post('/login',
#                                        data={"email":"admin","password":"admin","submit":"Login"},
#                                   follow_redirects=True
#                                   )
#
#            response = client.get('/delete_job_adv/25')
#
#            # response = client.get('/logout')
#            print(response.data)
#            self.assertEqual(response.status_code, 302)


#        def test_admin_users_can_delete_user(self):
#            client = app.test_client(self)
#            response = client.post('/login',
#                                        data={"email":"admin","password":"admin","submit":"Login"},
#                                   follow_redirects=True
#                                   )
#
#            response = client.get('/delete_user/15')
#
#            # response = client.get('/logout')
#            print(response.data)
#            self.assertEqual(response.status_code, 302)


#
#        def test_users_can_accept_job(self):
#            client = app.test_client(self)
#            response = client.post('/login',
#                                        data={"email":"fatih","password":"fatih","submit":"Login"},
#                                   follow_redirects=True
#                                   )
#
#            response = client.post('/response/22', data={"res":"Accept"},
#                                   follow_redirects=True)
#
#            # response = client.get('/logout')
#            print(response.data)
#            self.assertEqual(response.status_code, 200)
#
#
#        def test_users_can_reject_job(self):
#            client = app.test_client(self)
#            response = client.post('/login',
#                                        data={"email":"fatih","password":"fatih","submit":"Login"},
#                                   follow_redirects=True
#                                   )
#
#            response = client.post('/response/12', data={"res":"Reject"},
#                                   follow_redirects=True)
#
#            # response = client.get('/logout')
#            print(response.data)
#            self.assertEqual(response.status_code, 200)



        def test_matching_system(self):

            advertisement_details = Advertisement()
            advertisement_details.companydetail_id = 3
            advertisement_details.title = "Test Deneme"
            advertisement_details.description = "Test Desc"
            advertisement_details.date_posted = date.today()
            advertisement_details.deadline = date.today()

            keywords = get_keywords("java, python, c++", -1)

            advertisement_details.keywords = keywords

            get_matching(advertisement_details)

            # response = client.get('/logout')
            #print(response.data)
            self.assertTrue(len(advertisement_details.users) > 0)
        
        def test_check_email(self):
            email = 'ertugrulsmz55@gmail.com'
            control = is_email(email)
            self.assertTrue(control)

        def test_check_not_email(self):
            email = 'ertugrulsmz55@asdd'
            control = is_email(email)
            self.assertFalse(control)

        def test_user_have_business_keywords(self):
            aselsan = User.query.first()
            keywords = get_business_keywords(aselsan)
            
            self.assertIsNotNone(keywords)
            self.assertTrue(len(keywords)>0)

        def test_getkeywordfromdb_user_have_existing_keyword(self):
            student = User.query.filter_by(type = True).first()
            returned = get_keyword_from_db('Tensorflow',student.student_details)
            self.assertIsNone(returned)

        def test_getkeywordfromdb_user_not_have_existing_keyword(self):
            student = User.query.filter_by( type=True ).first()
            returned = get_keyword_from_db( 'java', student.student_details)

            self.assertIsNotNone(returned)
            self.assertIsNotNone(returned.id)

        def test_getkeywordfromdb_not_existing_keyword(self):
            student = User.query.filter_by( type=True ).first()
            returned = get_keyword_from_db( 'autocad', student.student_details )

            self.assertIsNotNone(returned)
            self.assertIsNone(returned.id)

        #almost same implementation, does not require extensive testing
        def test_getinterestfromdb_company_have_existing_interest(self):
            company = User.query.filter_by(type=False).first()
            returned = get_interest_from_db('Defence Industry',company.company_details)
            self.assertIsNone( returned )
        
        def test_getinterests_company_have_all(self):
            company = User.query.filter_by( type=False ).first()
            interest_array = get_interests("Electronics,Defence Industry",company.company_details)
            self.assertTrue(len(interest_array) == 0)

        def test_getinterests_company_doesnot_have_all(self):
            company = User.query.filter_by( type=False ).first()
            interest_array = get_interests( "Electronics,Bigdata", company.company_details )
            self.assertTrue( len( interest_array ) > 0)


        def test_getkeywords_student_have_all(self):
            student = User.query.filter_by( type=True ).first()
            keywords_array = get_keywords('Tensorflow,  opencv',student.student_details)
            self.assertTrue(len( keywords_array ) == 0)


        def test_getkeywords_student_doesnot_have_all(self):
            student = User.query.filter_by( type=True ).first()
            keywords_array = get_keywords( 'Tensorflow,  GAMS',student.student_details)
            self.assertTrue( len( keywords_array ) > 0)



    
    
    
    
    
    

if __name__ == '__main__':
    unittest.main()


