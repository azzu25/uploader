
# Django settings for webapp project.
from webapp.env_settings.base import *

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(PROJECT_ROOT,'uploaded/files/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dap_new',                    # Or path to database file if using sqlite3.
        'USER': 'writer',                      # Not used with sqlite3.
        'PASSWORD': 'writer',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

LOGGING['handlers']['error_log_handler'].update({'filename':'errors_log.log'})
LOGGING['handlers']['post_data_handler'].update({'filename':'post_data_log.log'})



