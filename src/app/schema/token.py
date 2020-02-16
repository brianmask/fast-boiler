""" Tokens! """

from pydantic import BaseModel


class Token(BaseModel):
    """ What is the token, what is the token's type? """

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """ Who does this token belong to? """

    sub: int = None
    iat: int = None
    exp: int = None
    max_exp: int = None
