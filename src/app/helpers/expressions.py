""" Reusable, centralized regular expressions """

import re

# Validate email address
VALID_EMAIL = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
