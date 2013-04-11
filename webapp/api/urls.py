from django.conf.urls.defaults import *


urlpatterns = patterns('webapp.api.views',
    url(r'^gettoken','get_token',name = 'gettoken_api'),
    url(r'^uploadmodel', 'modelupload',name='modelupload_api'),
    url(r'^dailylog', 'dailylog_upload',name='dailylog_api'),
    url(r'^masterdata', 'masterdata_upload',name='masterdata_api'),
    
)
