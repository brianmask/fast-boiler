""" password helpers """

import re

from passlib.context import CryptContext

from app.core import settings

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Pre compile all regular expressions for production performance
HAS_LOWERCASE = re.compile(r'[a-z]')
HAS_NUMERIC = re.compile(r'[0-9]')
HAS_UPPERCASE = re.compile(r'[A-Z]')

def get_password_hash(password: str) -> str:
    """ return hash of provided plain password """

    return PWD_CONTEXT.hash(password)

def has_lowercase(password: str) -> bool:
    """ checks if password has at least one lowercase character """

    return re.search(HAS_LOWERCASE, password) is not None

def has_numeric(password: str) -> bool:
    """ checks if password has at least one numeric character """

    return re.search(HAS_NUMERIC, password) is not None

def has_special_character(password: str) -> bool:
    """ checks if password has at least one special character """

    return any(char for char in password if not char.isalnum() and not char.isspace())

def has_uppercase(password: str) -> bool:
    """ checks if password has at least one uppercase character """

    return re.search(HAS_UPPERCASE, password) is not None

def validate_password(password: str) -> bool:
    """ validates the password ensuring it meets minimum requirements

    designed to be used inside a pydantic validator

    raises: ValueError if validation fails
    """

    # Ensure we have the minimum character count
    if len(password) < settings.MINIMUM_PASSWORD_LENGTH:
        raise ValueError(
            f'password must be at least {settings.MINIMUM_PASSWORD_LENGTH} characters'
        )

    complexity = 0
    password_complexity_checks = [has_lowercase, has_numeric, has_special_character, has_uppercase]

    for check in password_complexity_checks:
        if check(password) is True:
            complexity = complexity + 1

    if complexity < settings.MINIMUM_COMPLEXITY:
        raise ValueError(f'password must pass {settings.MINIMUM_COMPLEXITY} complexity checks')

    # All checks passed
    return True


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ verify plain password submitted by user matches stored hash """

    return PWD_CONTEXT.verify(plain_password, hashed_password)
