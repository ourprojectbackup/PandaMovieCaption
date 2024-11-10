#(©)CodeXBotz




import os
import logging
from logging.handlers import RotatingFileHandler


BASE_URL = "http://164.92.130.158:7000"

SECRET_CODE_LENGTH = 8

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7710510794:AAEpy_uVAclR4YCaTMiokGHZkinDx-3VK5k")
#TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7937806566:AAGJCTvDYunisFi3MsceemWqohtRvPinqIE")

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "12595500"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "e3b216e300f297f782f5984b462979a7")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001626866241"))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5351120371"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Test:1234@cluster0.2bzsp0q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002273264614"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", """Size of The File - {file_size}

Join 𝑼𝒔 : 👇

@PandaMoviesOFC2
𝘽𝙮 𝗠𝗢𝗛𝗔𝗡 🐼""")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
