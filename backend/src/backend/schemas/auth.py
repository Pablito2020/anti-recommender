from pydantic import BaseModel


class UserToken(BaseModel):
    access_token: str
    expires: int
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str


class MailPetition(BaseModel):
    mail: str
