import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)


# If using in your own project, update the project namespace below
from P_track.base import * 


SECRET_KEY = config['SECRET_KEY']

# False if not in os.environ
DEBUG = config['DEBUG']

ALLOWED_HOSTS = config['ALLOWED_HOSTS']


# Database settings
DATABASES = {
    'default': {
        'ENGINE': config['db']['ENGINE'],
        'NAME': config['db']['NAME'],
        'USER': config['db']['USER'],
        'PASSWORD': config['db']['PASSWORD'],
        'HOST': config['db']['HOST'],
        'PORT': config['db']['PORT'],
    }
}

# Email setting
EMAIL_HOST_USER=config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD=config['EMAIL_HOST_PASSWORD']

# # Amazon s3 settings

# AWS_S3_ACCESS_KEY_ID = config['aws_s3']['AWS_S3_ACCESS_KEY_ID']
# AWS_S3_SECRET_ACCESS_KEY = config['aws_s3']['AWS_S3_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = config['aws_s3']['AWS_STORAGE_BUCKET_NAME']

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_PRELOAD_METADATA = True

# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400'
# }
# AWS_HEADERS = { 
#     'Access-Control-Allow-Origin': '*',
# }


# AWS_LOCATION = 'static'
# AWS_QUERYSTRING_AUTH = False


# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'