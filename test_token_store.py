from services.token_store import get_token, is_token_saved

print("Token saved:", is_token_saved())
print("Token retrieved:", get_token() is not None)