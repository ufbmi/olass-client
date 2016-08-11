"""
Goal: store application settings
"""
TOKEN_URL = 'https://localhost'
SAVE_URL = 'https://localhost'


DB_NAME = ''
# DB_URL_TESTING = 'sqlite:///:memory:'
DB_URL_TESTING = 'sqlite:///db.sqlite'

# Partners should only add/remove elements to this array
# to activate/deactivate hashing rules
ENABLED_RULES = ['F_L_D_Z', 'L_F_D_Z', 'F_L_D_C', 'L_F_D_C']
