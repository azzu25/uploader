"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest
import json
from django.test import Client
from django.contrib.auth.models import User
import os

PATH = os.path.realpath(os.path.dirname(__file__))

class ModelUpLoadTestCase(unittest.TestCase):
    def setUp(self):
        User.objects.create_user('testuser', 'testuser@gmail.com', 'testuser')
        self.client = Client()
        resp = self.client.post('/api/v1/gettoken',{'username':'testuser','password':'testuser'})
        resp_dict = json.loads(resp.content)
        self.token = resp_dict['token']
        self.userid = resp_dict['user']
        file_obj = open(PATH+'test.xlxs','rb')
        self.file = file_obj

    def test_without_transactiontype(self):
        post_dict = {'model_file':self.file,
                     'token':self.token,'user':self.userid}
        result = {'status': 'error', 'message':'transactiontype missing or invalid.'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)
 
    def test_allowed_Tran_type_with_modelFile_without_ticker(self):
        post_dict = {'model_file':self.file,
                     'token':self.token,'user':self.userid,
                     'transactiontype':'MODEL_INITIAL'}
        result = {'status': 'error', 'message': 'companyticker is mandatory.'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_allowed_Tran_type_without_modelFile_with_ticker(self):
        post_dict = {'token':self.token,'user':self.userid,'companyticker':'BA',
                     'transactiontype':'MODEL_INITIAL'}
        result = {'status': 'error', 'message':'model_file is mandatory for MODEL_INITIAL.'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_not_allowed_Tran_type_without_modelFile_with_ticker(self):
        post_dict = {'companyticker':'BA',
                     'token':self.token,'user':self.userid,
                     'transactiontype':'UNRESTRICT'}
        result = {'status': 'success'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)
 
    def test_not_allowed_Tran_type_with_modelFile_with_ticker(self):
        post_dict = {'companyticker':'BA','model_file':self.file,
                     'token':self.token,'user':self.userid,
                     'transactiontype':'MODEL_INITIAL'}
        result = {'status': 'success'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_not_allowed_Tran_type_with_modelFile_without_ticker(self):
        post_dict = {'model_file':self.file,
                     'token':self.token,'user':self.userid,
                     'transactiontype':'MODEL_INITIAL'}
        result = {'status': 'error', 'message': 'companyticker is mandatory.'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_allowed_Tran_type_with_modelFile_with_ticker_neg(self):
        post_dict = {'model_file':self.file,'companyticker':'BA',
                     'token':self.token,'user':self.userid,
                     'transactiontype':'MODEL_INITIAL'}
        result = {'status': 'error'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertNotEqual(result, response)

    def test_not_allowed_Tran_type_without_modelFile_with_ticker_neg(self):
        post_dict = {'companyticker':'BA',
                     'token':self.token,'user':self.userid,
                     'transactiontype':'UNRESTRICT'}
        result = {'status': 'error'}
        response = self.client.post('/api/v1/uploadmodel',post_dict)
        response = json.loads(response.content)
        self.assertNotEqual(result, response)

    def test_dailylog_with_logfile_and_mandtryfields(self):
        post_dict = {'log_file':self.file,'filename':'test.log','filesize':200,'md5hash':'1234566',
                     'token':self.token,'user':self.userid}
        result = {'status': 'success'}
        response = self.client.post('/api/v1/dailylog',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)
  
    def test_dailylog_without_logfile_and_mandtryfields(self):
        post_dict = {'filename':'test.log','filesize':200,'md5hash':'1234566',
                     'token':self.token,'user':self.userid}
        result = {'status': 'error', 'message': 'log_file is mandatory'}
        response = self.client.post('/api/v1/dailylog',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_dailylog_with_logfile_and_without_mandtryfield(self):
        post_dict = {'log_file':self.file,'filename':'test.log','filesize':200,
                     'token':self.token,'user':self.userid}
        result = {'status': 'error', 'message':'filename, md5hash, filesize are mandatory fields'}
        response = self.client.post('/api/v1/dailylog',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_masterdata_with_logfile_and_mandtryfields(self):
        post_dict = {'master_file':self.file,'filename':'test.log','filesize':200,'md5hash':'1234566',
                     'token':self.token,'user':self.userid}
        result = {'status': 'success'}
        response = self.client.post('/api/v1/masterdata',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_masterdata_without_logfile_and_mandtryfields(self):
        post_dict = {'filename':'test.log','filesize':200,'md5hash':'1234566',
                     'token':self.token,'user':self.userid}
        result = {'status': 'error', 'message': 'master_file is mandatory'}
        response = self.client.post('/api/v1/masterdata',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)

    def test_masterdata_with_logfile_and_without_mandtryfield(self):
        post_dict = {'master_file':self.file,'filename':'test.log','filesize':200,
                     'token':self.token,'user':self.userid}
        result = {'status': 'error', 'message':'filename, md5hash, filesize are mandatory fields'}
        response = self.client.post('/api/v1/masterdata',post_dict)
        response = json.loads(response.content)
        self.assertEqual(result, response)
    
    def test_dailylog_without_logfile_and_without_mandtryfields(self):
        post_dict = {'token':self.token,'user':self.userid}
        result = {'status': 'error', 'message': 'log_file is mandatory'}
        response = self.client.post('/api/v1/dailylog',post_dict)
        response = json.loads(response.content)
        self.assertNotEqual(result, response)

    def test_masterdata_without_logfile_and_without_mandtryfields(self):
        post_dict = {'token':self.token,'user':self.userid}
        result = {'status': 'error', 'message': 'log_file is mandatory'}
        response = self.client.post('/api/v1/masterdata',post_dict)
        response = json.loads(response.content)
        self.assertNotEqual(result, response)

    def tearDown(self):
        User.objects.all().delete()
