"""
Goal: store application settings
"""

# Set to False if the a target server has a self-signed certificate
VERIFY_SSL_CERT = False

CLIENT_ID = 'client_1'
CLIENT_SECRET = 'secret_1'

# Application endpoints
TOKEN_URL = 'https://localhost:5000/oauth/token'
SAVE_URL = 'https://localhost:5000/api/save'

DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'olassc'
DB_USER = 'olassc'
DB_PASS = 'insecurepassword'

# ##############################################
# Params used while running run_data_import.py #
# ##############################################
# @see utils:process_frame()
SEND_TO_DB = True
