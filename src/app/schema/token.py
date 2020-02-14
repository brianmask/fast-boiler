""" Tokens! """

from pydantic import BaseModel


class Token(BaseModel):
    """ What is the token, what is the token's type? """

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """ Who does this token belong to? """

    user_id: int = None
