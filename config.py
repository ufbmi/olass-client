"""
Goal: store application settings
"""

# Set to False if the a target server has a self-signed certificate
VERIFY_SSL_CERT = False

#
CLIENT_ID = 'client_1'
CLIENT_SECRET = 'secret_1'

# TOKEN_BASE_URL = 'https://localhost:5000/oauth/token'
# SECURE_DATA_URL = 'https://localhost:5000/api/me'

# Application endpoints
TOKEN_URL = 'https://ahc-olass19b.ahc.ufl.edu/oauth/token'
SAVE_URL = 'https://ahc-olass19b.ahc.ufl.edu/api/save'

SEND_TO_DB = True

DB_HOST = 'localhost'
DB_PORT = 3306

DB_NAME = 'olassc'
DB_USER = 'olassc'
DB_PASS = 'insecurepassword'
