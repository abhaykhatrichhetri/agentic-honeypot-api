API_KEY = "mysecretkey123"

def verify_api_key(auth_header: str):
    if not auth_header:
        return False

    if not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ")[1]
    return token == API_KEY
