from os import environ


# reading a token from .txt file
def get_from_txt(file_name: str) -> str:
    try:
        f = open(file_name, "r")
    except:
        raise FileNotFoundError(f"{file_name} not found!")
    token = f.read()
    if token != "":
        return token
    raise ValueError(f"Token not found in {file_name}!")
    
# environ["BOT_TOKEN"] = "1"
# environ["QIWI_TOKEN"] = "2"

def check_environ(tokens: list):
    if all(x in environ for x in tokens):
        return True
    return False

# for name, value in environ.items():
#     print("{0}: {1}".format(name, value))

tokens = ["BOT_TOKEN", "QIWI_TOKEN"]
a = check_environ(tokens)


# TODO: if all(x in os.environ for x in["BOT_TOKEN", "QIWI_TOKEN"])
if "BOT_TOKEN" in environ and "QIWI_TOKEN" in environ:
    bot_token = environ.get("BOT_TOKEN")
    qiwi_token = environ.get("QIWI_TOKEN")
else:
    bot_token = get_from_txt("bot_token.txt")
    qiwi_token = get_from_txt("qiwi_token.txt")
    
    

def get_secrets(path):
  qiwi_token = environ.get('QIWI_TOKEN')
  tg_token = environ.get('TG_TOKEN')
  
  if qiwi_token and tg_token:
    # Both environment variables exist, return them as a tuple
    return (qiwi_token, tg_token)
  
  # One or both environment variables do not exist, try reading from file
  try:
    with open(path, 'r') as f:
      qiwi_token = f.readline().strip()
      tg_token = f.readline().strip()
      
      if qiwi_token and tg_token:
        # Both tokens found in file, return them as a tuple
        return (qiwi_token, tg_token)
      
      # Only one token found in file
      elif qiwi_token:
        raise "QIWI_TOKEN found in file, but TG_TOKEN not found"
      elif tg_token:
        raise "TG_TOKEN found in file, but QIWI_TOKEN not found"
      else:
        # No tokens found in file
        raise "QIWI_TOKEN and TG_TOKEN not found in file"
  except FileNotFoundError:
    # File not found, raise an error with the full path
    raise Exception(f"File not found: {path}")