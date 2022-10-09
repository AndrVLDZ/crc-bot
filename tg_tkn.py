bot_access_token = None

# reading a token
def get() -> None:
    try:
        f = open('tg_token.txt', 'r')
        global bot_access_token
        bot_access_token = f.read()
        if not bot_access_token:
            print('Токен не найден! \nНеобходимо сохранить токен в tg_token.txt в папке программы')
    except:
        print('Токен не найден! \nНеобходимо создать файл tg_token.txt в папке программы и сохранить в нём токен') 

get()