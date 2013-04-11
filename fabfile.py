from fabric.api import local, task, run, env, cd, put, hosts, sudo
from fabric.contrib.project import rsync_project
    
DEV_SERVER = 'jenkins@192.168.2.32'
        
CODE_PATH = {
    'dev':'uploader'
}            
    
ENV_SETTINGS = {
    'dev':'dev.py'
}
    
WSGI_FILES = {
    'dev': 'dev.wsgi'
}    

@task  
@hosts(DEV_SERVER)
def dev(user=None):
    if user:
        env.user = user
    run_tests()
    push_code_to_server('dev')

def run_tests():
    local('python manage.py test')

def generate_version_hash():
    local('python manage.py hash_generator')

def copy_settings_file(environment):
    try:
        new_settings = ENV_SETTINGS[environment]
    except:
        return            
                
    with cd('C:/%s/webapp' % CODE_PATH.get(environment)):
        run('cp env_settings/%s settings.py' % new_settings)
        if environment in WSGI_FILES:
            run('cp C:/uploader/wsgi/%s C:/uploader/apache/uploader.wsgi' %
                WSGI_FILES[environment])


def push_code_to_server(environment):    
    remote_path = 'C:/uploader/%s' % CODE_PATH.get(environment)
    exclude = ('.*', '*.pyc', '*.json')
    with cd('C:/uploader'):
        sudo('chmod -R 775 %s/' % remote_path)
        sudo('chown -R %s %s/' % (env.user, remote_path))
        #sudo('chmod -R 775 logs/')
        #sudo('chgrp -R admin logs/')

    #do not delete the json files
    rsync_project(remote_path, '.', exclude=exclude)
    
    copy_settings_file(environment)
    
    with cd('C:/%s' % CODE_PATH.get(environment)):
        run('touch apache/uploader.wsgi')
