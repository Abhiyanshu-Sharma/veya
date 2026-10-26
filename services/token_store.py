
import keyring


SERVICE_NAME = "Veya"


def save_token(token):
    keyring.set_password(SERVICE_NAME, "github_access_token", token)


def get_token():
    return keyring.get_password(SERVICE_NAME, "github_access_token")


def is_token_saved():
    return get_token() is not None


def delete_token():
    keyring.delete_password(SERVICE_NAME, "github_access_token")
