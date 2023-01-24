from pyrogram import filters, Client
from traceback import format_exc
from typing import Tuple
import asyncio
import random
from pyrogram import Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import (
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message)
from Darmiubot.config import *
from Darmiubot.utilities.data import *
from Darmiubot.utilities.mongo import * 


@Client.on_message( ~filters.me & filters.incoming)
async def watch_raids(client: Client, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    user = message.from_user.id
    kaal = random.choice(REPLY_RAID)
    love = random.choice(LOVER_RAID)
    if int(user) in VERIFIED_USERS:
        return
    elif int(user) in SUDO_USERS:
        return
    if int(message.chat.id) in GROUP:
        return
    if await kaalub_info(user):
        try:
            await message.reply_text(kaal)
        except:
            return
    if await loveub_info(user):
        try:
            await message.reply_text(love)
        except:
            return




__MODULE__ = "Rᴀɪᴅ"
__HELP__ = f"""
**Cinta Raid dan Balas Raid**

**ᴜsᴀɢᴇ:**
`.lraid` - ** Balas pesan seseorang untuk mengaktifkan Raid Cinta**

`.dlraid` - ** Balas pesan seseorang untuk menonaktifkan Raid Cinta.**

`.rraid` - ** Balas pesan seseorang untuk mengaktifkan Raid Cinta.**

`.drraid` - ** Balas pesan seseorang untuk menonaktifkan Raid Balasan.**
"""
