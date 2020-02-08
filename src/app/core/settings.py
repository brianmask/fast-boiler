""" Centralized place to store any configurable application settings """

import os

# Database Settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Password Settings
MINIMUM_PASSWORD_LENGTH = 8
MINIMUM_COMPLEXITY = 3
