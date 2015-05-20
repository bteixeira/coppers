import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from coppersprj.settings import *

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'ec2-54-217-202-108.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
        'NAME': 'd85nuui9nd0p2t',
        'USER': 'jqgahjjqztpuaq',
        'PASSWORD': 'zNCFxN3HP2zbvk_7VyzQhaCnNi',
    }
}
