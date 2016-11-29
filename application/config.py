import os

DEBUG = True

if os.getenv('VERIFY') == 'True':
    VERIFY = True
else:
    VERIFY = False

DEED_API_BASE_HOST = os.getenv('DEED_API_ADDRESS',
                               'http://0.0.0.0:9020')

GOOGLE_ANALYTICS_CODE = os.getenv('GOOGLE_ANALYTICS_CODE',
                                  'UA-59849906-6')

APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', 'dm-session-key')

AKUMA_BASE_HOST = os.getenv('AKUMA_ADDRESS',
                            'http://127.0.0.1:5055')
