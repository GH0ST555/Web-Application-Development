import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models
from .models import User , Product


def add(x,y):
    return x + y

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass



    def test_login_load(self):
       response = self.app.get('/login',follow_redirects=True)
       self.assertEqual(response.status_code, 200)



    def test_login_auth(self):
       response = self.app.get('/login',follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def test_create_account(self):
       response = self.app.get('/create_account',follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def test_addtaskroute(self):
       response = self.app.get('/',follow_redirects=True)
       self.assertEqual(response.status_code, 200)

    def tearDown(self):
        db.session.remove()
        db.drop_all()   

if __name__ == '__main__':
    unittest.main()
