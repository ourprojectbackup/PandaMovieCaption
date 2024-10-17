from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
import re
@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

@Bot.on_message(filters.command('share') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):

    while True:
        try:
            first_message = await bot.ask(text = "Send the Poster", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
            if(first_message.text=="."):
                break
            caption = first_message.caption
            lines = caption.split("\n")
            name= lines[0]
            movie = re.sub(r' - \(\d{4}\)', '', name)
            word_list = movie.split()    
            for key in word_list:
                await first_message.reply_text(f"/add  {key}",quote = True)
                await first_message.reply_text(f"/filter  {key}",quote = True)

            await first_message.reply_text("/broadcast",quote = True)
            
        except:
            return


@Bot.on_message(filters.private & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)
