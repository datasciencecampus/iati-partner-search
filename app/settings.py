import os
import random
import string
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(dotenv_path)

FLASK_ENV = os.getenv("FLASK_ENV", "changeme").lower()

if FLASK_ENV == "production":
    SECRET_KEY = os.getenv("APP_SECRET_KEY")
    FLASK_DEBUG = False
elif FLASK_ENV == "development":
    SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    FLASK_DEBUG = True
else:
    raise Exception("FLASK_ENV is incorrectly configured\n\nCheck you .env file\n\nMust be either 'FLASK_ENV=production' or 'FLASK_ENV=development'")

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
