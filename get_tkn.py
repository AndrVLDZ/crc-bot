# reading a token from .txt file
def get(file_name: str) -> str:
    try:
        f = open(file_name, 'r')
        token = f.read()
        if not token:
            print(f'Token not found! \nAdd your token to {file_name} in the program folder')
        else:
            return token
    except:
        print('Token not found! \nCreate a {file_name} file in the program folder and add your token to it') 