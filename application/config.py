import os

DEBUG = True

VERIFY = os.getenv('VERIFY',
                   False)

DEED_API_BASE_HOST = os.getenv('DEED_API_ADDRESS',
                               'http://0.0.0.0:9020')

GOOGLE_ANALYTICS_CODE = os.getenv('GOOGLE_ANALYTICS_CODE',
                                  'UA-59849906-6')

APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', 'dm-session-key')
