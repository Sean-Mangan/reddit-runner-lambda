# Helpful little class for storing credentials
import os

from secrets_utils import set_secrets

# Grab the secrets from asm before storing them as attributes
set_secrets()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USER_NAME = os.environ["USER_NAME"]
PASSWORD = os.environ["PASSWORD"]