#----------IMPORTS---------
import os
from logic import InstaFollower
from dotenv import load_dotenv
load_dotenv()



#--------CONSTANTS---------
SIMILAR_ACCOUNT = os.getenv("SIMILAR_ACCOUNT")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
INSTA_LOGIN_URL = "https://www.instagram.com/accounts/login/"
TARGET_ACCOUNT = os.getenv("TARGET_ACCOUNT")

#-------MAIN CODE-------

follower_bot = InstaFollower()
follower_bot.login(INSTA_LOGIN_URL,USER_NAME,PASSWORD)
follower_bot.find_followers(TARGET_ACCOUNT)
# follower_bot.follow()




