import site
import os
import sys

sys.stdout = sys.stderr

#new_path = '/var/www/env/UPLOADER/lib/python2.7/site-packages'

#prev_sys_path = list(sys.path)
# add the site-packages of our virtualenv as a site dir
#site.addsitedir(new_path)
# add the app's directory to the PYTHONPATH
sys.path.append('C:/uploader/webapp')
sys.path.append('C:/uploader')

# reorder sys.path so new directories from the addsitedir show up first
#new_sys_path = [p for p in sys.path if p not in prev_sys_path]
#for item in new_sys_path:
 #   sys.path.remove(item)
#sys.path[:0] = new_sys_path

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

