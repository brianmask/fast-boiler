""" Centralized place to store any configurable application settings """

import os

# Secret Key - really... keep this a secret
SECRET_KEY = os.getenvb(b'SECRET_KEY', 'DoNotRunThisInProductionWithoutSettingAProperSecretKey!!!')

# Database Settings
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')

# Password Settings
MINIMUM_PASSWORD_LENGTH = os.environ.get('MINIMUM_PASSWORD_LENGTH', 8)
MINIMUM_COMPLEXITY = os.environ.get('MINIMUM_COMPLEXITY', 3)

# JWT Settings
JWT_EXPIRATION_TIME = os.environ.get('JWT_EXPIRATION_TIME', 60 * 30)  # Expiration delta in seconds
JWT_MAXIMUM_LIFETIME = os.environ.get('JWT_MAXIUMUM_LIFETIME', 60 * 60 * 24 * 365) # Max lifetime
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_SUBJECT = os.getenv('JWT_SUBECT', 'access')

# First Superuser
FIRST_USER = os.getenv('FIRST_USER', 'user')
FIRST_PASSWORD = os.getenv('FIRST_PASSWORD', 'p@55w0rd')
