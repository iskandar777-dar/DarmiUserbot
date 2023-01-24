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
from Darmiubot.modules.helpers.filters import *
from Darmiubot.modules.helpers.decorators import errors, sudo_users_only
from Darmiubot.modules.helpers.program import get_arg
from Darmiubot.modules.helpers.admins import CheckAdmin


@Client.on_message(command("gcast"))
@errors
@sudo_users_only
async def gbroadcast(client: Client, message: Message):
    msg_ = await message.edit_text("`Memproses..`")
    failed = 0
    if not message.reply_to_message:
        await msg_.edit("`Balas Pesannya anjay!`")
        return
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    await msg_.edit("`Sekarang Mengirim Ke Semua Obrolan!`")
    if not chat_dict:
        msg_.edit("`Anda Tidak Memiliki Obrolan!`")
        return
    for c in chat_dict:
        try:
            msg = await message.reply_to_message.copy(c)
        except:
            failed += 1
    await msg_.edit(
        f"`Pesan Berhasil Kirim Ke {chat_len-failed} Obrolan! Gagal Masuk {failed} Obrolan.`"
    )


__MODULE__ = "Gʟᴏʙᴀʟ"
__HELP__ = f"""
**Gʙᴀɴ & Gᴍᴜᴛᴇ Mᴏᴅᴜʟᴇ**

**penggunaan :**
`.gmute` - ** Balas Pesan untuk Global bisu.**

`.ungmute` - ** Balas Pesan untuk Membuka Global Bisu.**

`.gban` - ** Balas Pesan untuk Global Banned.**

`.ungban` - ** Balas Pesan untuk Membuka Global Banned.**

`.gcast` - ** Balas Pesan untuk Global Brodacast**
"""
