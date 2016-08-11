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

# Partners should only add/remove elements to this array
# to activate/deactivate hashing rules
ENABLED_RULES = ['F_L_D_Z', 'L_F_D_Z', 'F_L_D_C', 'L_F_D_C']
