# reading a token from .txt file
def get(file_name: str) -> str:
    try:
        f = open(file_name, "r")
    except:
        raise FileNotFoundError("Token file not found!")
    token = f.read()
    if token != "":
        return token
    else: 
        raise ValueError("Token not found in file!")