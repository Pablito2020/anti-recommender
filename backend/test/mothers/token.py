from src.backend.spotify.domain import Token


def get_token_that_expires_on(expires_at: float) -> Token:
    return Token(
        access_token="access_token",
        token_type="token_type",
        expires_in=100,
        refresh_token="refresh_token",
        scope="scope",
        id_token="id_token",
        expires_at=expires_at,
    )
