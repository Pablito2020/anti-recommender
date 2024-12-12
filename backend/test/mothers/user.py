from backend.services.spotify.users.domain import User, Mail


def get_user(mail: str, creation_date: float = 1000) -> User:
    return User(mail=Mail(address=mail), creation_date=creation_date)


def get_mail(user: User) -> str:
    return user.mail.address
