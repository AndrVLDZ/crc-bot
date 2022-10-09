api_access_token = None

# reading a token
def get() -> None:
    try:
        f = open('qiwi_token.txt', 'r')
        global api_access_token
        api_access_token = f.read()
        if not api_access_token:
            print('Токен не найден! \nНеобходимо сохранить токен в qiwi_token.txt в папке программы')
    except:
        print('Токен не найден! \nНеобходимо создать файл qiwi_token.txt в папке программы и сохранить в нём токен') 

get()