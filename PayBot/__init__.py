import asyncio
import time
import sys
import logging
import logging.handlers as handlers
from motor import motor_asyncio
from pyrogram import Client
from config import Settings


loop = asyncio.get_event_loop()
boot = time.time()

logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              handlers.RotatingFileHandler("bot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)

logging.getLogger("pyrogram").setLevel(logging.ERROR)

bot = Client(
    ":cbot:",
    api_id=Settings.API_ID,
    api_hash=Settings.API_HASH,
    bot_token=Settings.BOT_TOKEN,
    # plugins = {"root": "Modules/plugins"}
)


client = motor_asyncio.AsyncIOMotorClient(Settings.MONGO_URI)
db = client["RazorBot"]
ChatDB = db["Chats_DB"]
UserDB = db["User_DB"]
BotDB = db["BOT_DB"]


LOG_GROUP = Settings.LOG_GROUP

async def cbot_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await bot.start()
    try:
        await bot.send_message(int(LOG_GROUP), text= "Bot started successfully!")
    except Exception as e:
        print("Please add to your log group, and give me administrator powers!")
        print(f"Error: {e}")
    
    getme = await bot.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    print(BOT_ID, BOT_NAME, BOT_USERNAME)

loop.run_until_complete(cbot_bot())
