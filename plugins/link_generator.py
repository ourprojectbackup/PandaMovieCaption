#(©)Codexbotz

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id
import requests
import re

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    long_link = f"https://t.me/{client.username}?start={base64_string}"
    link = shorten_link(long_link)
 # Now retrieve all messages between the first and last message IDs from the DB channel
    files_list = []
    found_languages = set()
    found_year = set()
    found_moviename = set()

    for msg_id in range(f_msg_id, s_msg_id + 1):
        try:
            msg = await client.get_messages(chat_id=client.db_channel.id, message_ids=msg_id)
            
            # Check if the message contains media (documents, videos, etc.)
            if msg.document or msg.video:
                file_size = msg.document.file_size if msg.document else msg.video.file_size
                file_name = msg.document.file_name if msg.document else msg.video.file_name
                file_caption = msg.caption 

                year = extract_year_from_caption(file_name)
                if year:
                    found_year.add(year)

                movie = extract_movie_name(file_name)
                if movie:
                    found_moviename.add(movie)

                language_map = {
                    "TAMIL": "Tam",
                    "TELUGU": "Tel",
                    "HINDI": "Hin",
                    "KOREAN": "Kor",
                    "MALAYALAM": "Mal",
                    "KANNADA": "Kan",
                    "ENGLISH": "Eng",
                    "BENGALI": "Ben",
                    "MARATHI": "Mar"
                }

                caption_upper=""

                if file_name:
                    caption_upper = file_name.upper()
                else:
                    caption_upper = ""

                if file_caption:
                    caption_upper += file_caption.upper()

                for full_lang, short_lang in language_map.items():
                    if full_lang in caption_upper or short_lang.upper() in caption_upper:
                        found_languages.add(full_lang)

               
                       


                # Convert file size to MB or GB
                if file_size >= 1024 * 1024 * 1024:  # Greater than or equal to 1 GB
                    size_str = f"{file_size / (1024 * 1024 * 1024):.2f} GB"
                else:
                    size = file_size / (1024 * 1024)
                    size_str = f"{round(size / 50) * 50} MB"

                # Store file details (size, link) in a list for sorting
                files_list.append((file_size, f"{size_str}"))

        except Exception as e:
            await message.reply(f"❌ Failed to get message ID: {msg_id}. Error: {str(e)}", quote=True)
            continue

    # Sort the files based on file size (ascending order)
    files_list.sort(key=lambda x: x[0])  # Sort by file_size

    # Separate sorted files into TELEGRAM_FILES and WATCH_ONLINE/ DOWNLOAD
    telegram_files = []
    online_files = []
    for i, file_info in enumerate(files_list):
        
        telegram_files.append( f"{file_info[1]} : {link}" )
        
        online_files.append(f"{file_info[1]} : ")

    # Create the caption format similar to your provided one
    caption = ""

    if found_moviename:
        caption +=f"{list(found_moviename)[0]} - "
    else:
        caption +="   "

    if found_year:
        caption +=f"({list(found_year)[0]})\n\n"
    else:
        caption +="()\n\n"

    if found_languages:
        hashtags = " ".join([f"#{lang}" for lang in found_languages])
        caption += f"{hashtags} #HD\n\n"
 

    caption += "▬▬▬▬▬(#TELEGRAM_FILES)▬▬▬▬▬\n\n"
    for file in telegram_files:
        caption +="\n"+ file + "\n"
    
    caption += "\n▬▬(#WATCH_ONLINE/#DOWNLOAD)▬▬\n\n"
    for file in online_files:
        caption +="\n"+ file + "\n"
    
    # Add Footer
    caption += "\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
    caption += "🧡🤍💚 Hᴏᴡ Tᴏ DᴏᴡɴLᴏᴀᴅ  🧡🤍💚\n\n"
    caption += "𝐋𝐢𝐧𝐤 : @How_To_Download_Panda_Movies\n\n"
    caption += "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
    caption += "@PandaMoviesOFC"

    # Reply with the generated caption
   

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={long_link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{long_link}", quote=True, reply_markup=reply_markup)
    await second_message.reply_text(caption, quote=True)

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)




def shorten_link(long_url, alias=None):
    # Your API token
    api_token = "af341e8102ca4b5fa1ee430fe09b3ad0893f8b25"
    
    # Base URL of ModiJiUrl API
    api_url = "https://modijiurl.com/api"
    
    # Parameters for the API request
    params = {
        "api": api_token,
        "url": long_url,
        "format": "text"  # To get just the shortened link in text format
    }
    
    # Add alias if provided
    if alias:
        params["alias"] = alias
    
    # Send GET request to the API
    response = requests.get(api_url, params=params)
    
    # Check for successful response
    if response.status_code == 200:
        short_link = response.text.strip()  # Shortened URL in text format
        return short_link
    else:
        return f"Error: {response.status_code}"
    





def extract_year_from_caption(caption):
    # Regular expression to find a 4-digit year (between 1900 and 2099)
    year_pattern = r"\b(19[0-9]{2}|20[0-9]{2})\b"
    
    # Search for the year using the regex pattern
    match = re.search(year_pattern, caption)
    
    if match:
        return match.group(0)  # Return the found year as a string
    else:
        return None
    


def extract_movie_name(file_name):
    cleaned_name = re.sub(r'\s*@\S*\s*-\s*-*\s*', ' - - ', file_name)
    
    # Find the index of the opening parenthesis
    open_paren_index = cleaned_name.find('(')
    
    if open_paren_index != -1:
        # Extract and return the movie name (trim any leading/trailing spaces)
        movie_name = cleaned_name[:open_paren_index].strip()
        return movie_name
    else:
        return None
    
