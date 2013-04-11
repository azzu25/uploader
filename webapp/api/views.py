from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import json
from tokenapi.views import token_new
from tokenapi.decorators import token_required
import logging, traceback, sys
from datetime import datetime

from metadump import dump_meta_data
error_logger = logging.getLogger('error_log')
post_data_log = logging.getLogger('post_data_logger')


def error_log():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traces = traceback.extract_tb(exc_traceback)
    stack_trace = [str(exc_value)]
    for trace in traces:
        stack_trace.append(' '.join(str(i) for i in trace))
    error_logger.error('\n\t'.join(stack_trace))
    return True

@csrf_exempt           
def get_token(request):
    if request.method == 'POST':
        try:
            httpresponse = token_new(request)
        except:
            error_log()
            resp = {'status': 'error', 'message':'Invalid user.'}
        return httpresponse
    else:
        error_log()
        resp = {'status': 'error', 'message':'Must access via a POST request.'}
        return HttpResponse(json.dumps(resp, indent=4))   

@token_required
def modelupload(request):
    resp ={}
    resp['status'] = 'success'
    allowed_tran_types = ['MODEL_UPDATE','MODEL_INITIAL','MODEL_CORRECTION']
    transactiontypes = ['MODEL_UPDATE','MODEL_INITIAL','MODEL_CORRECTION',
                        'REAFFIRM','DROP_COVERAGE','RESTRICT','REVIEW',
                        'REVIEW_EXTENDED','UNRESTRICT','OTHER_UPDATE']
    if request.method == 'POST':
        tran_type = None
        post_data_dict = get_dict_lowercase(request.POST)
        file_data_dict = get_dict_lowercase(request.FILES)
        try:
            user_name = request.user.username
            post_data = ''
            for key,value in post_data_dict.iteritems():
                key , value = key.encode(), value.encode()
                if key !='token':
                    post_data  = post_data + '|' + key +':'+ value
            if post_data:
                log_data = 'username - '+ user_name + '  ' + post_data
                post_data_log.info(log_data)

            tran_type = post_data_dict.get("transactiontype")
            ticker = post_data_dict.get("companyticker")
            if not tran_type or tran_type not in transactiontypes:
                resp = {'status': 'error', 'message':'transactiontype missing or invalid.'}
            elif not ticker:
       	        resp = {'status': 'error', 'message':'companyticker is mandatory.'}
            else:
                data = file_data_dict.get('model_file')
                if tran_type in allowed_tran_types and not data:
                    resp = {'status': 'error', 'message':'model_file is mandatory for %s.' % (tran_type)}
                elif data:
                    name =  data.name
                    default_storage.save(user_name +'/'+name, ContentFile(data.read()))
                fname = ticker+'_'+tran_type+'_'+datetime.now().strftime("%Y%m%d%H%M%S")
                dump_meta_data(post_data_dict, user_name, fname)
        except Exception as e:
            error_log()
            resp = {'status': 'error', 'message':'file uploading error.'}
    else:
        resp = {'status': 'error', 'message':'Must access via a POST request.'}
    return HttpResponse(json.dumps(resp, indent=4))   

def get_dict_lowercase(inp_dict):
    resp = {}
    for key,value in inp_dict.iteritems():
        key = key.encode()
        resp[key.lower()] = value
    return resp

def validate_mandatory_fields(data_dict, fields):
    for f in fields:
        if not data_dict.get(f):
            return False
    return True

@token_required
def dailylog_upload(request):
    resp = {}
    resp['status'] = 'success'
    mandatory_fields = ['filename','md5hash','filesize']
    if request.method == 'POST':
        user_name = request.user.username
        try:
            post_data_dict = get_dict_lowercase(request.POST)
            file_data_dict = get_dict_lowercase(request.FILES)
            if not validate_mandatory_fields(post_data_dict, mandatory_fields):
                resp = {'status': 'error', 'message':'%s are mandatory fields' % (', '.join(mandatory_fields))}
            else:
                data = file_data_dict.get('log_file')
                if not data:
                    resp = {'status': 'error', 'message': 'log_file is mandatory'}
                else:
                    file_save('dailylog', user_name, data)
        except:
            error_log()
            resp = {'status': 'error', 'message':'file uploading error.'}
    else:
        resp = {'status': 'error', 'message':'Must access via a POST request.'}
    return HttpResponse(json.dumps(resp, indent=4))

@token_required
def masterdata_upload(request):
    resp = {}
    resp['status'] = 'success'
    mandatory_fields = ['filename','md5hash','filesize']
    if request.method == 'POST':
        user_name = request.user.username
        try:
            post_data_dict = get_dict_lowercase(request.POST)
            file_data_dict = get_dict_lowercase(request.FILES)
            if not validate_mandatory_fields(post_data_dict, mandatory_fields):
                resp = {'status': 'error', 'message':'%s are mandatory fields' % (', '.join(mandatory_fields))}
            else:
                data = file_data_dict.get('master_file')
                if not data:
                    resp = {'status': 'error', 'message': 'master_file is mandatory'}
                else:
                    file_save('masterdata', user_name, data)
        except:
            error_log()
            resp = {'status': 'error', 'message':'file uploading error.'}
    else:
        resp = {'status': 'error', 'message':'Must access via a POST request.'}
    return HttpResponse(json.dumps(resp, indent=4))

def file_save(dailylog_or_masterdata, username, data):
    file_name = username+'/'+dailylog_or_masterdata+'_'+datetime.now().strftime("%Y%m%d%H%M%S")
    default_storage.save(file_name, ContentFile(data.read()))
