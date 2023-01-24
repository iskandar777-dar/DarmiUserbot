import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Darmiubot.modules.clientbot.clientbot import client
from Darmiubot.modules.helpers.command import commandpro
from Darmiubot.modules.helpers.decorators import sudo_users_only, errors
from Darmiubot.utilities.misc import SUDOERS

@Client.on_message(commandpro(["op", "x", ".op", "wow", "nice", "beautiful"]) & filters.me)
async def downloader(_, message: Message):
    targetcontent = message.reply_to_message
    downloadtargetcontent = await client.download_media(targetcontent)
    send = await client.send_document("me", downloadtargetcontent)
    os.remove(downloadtargetcontent)


__MODULE__ = "Sᴇʟғ"
__HELP__ = f"""
**unduh media penghancur diri apa pun dan simpan ke pesan simpanan Anda**

**ᴜsᴀɢᴇ:**
`op|.op` - **Balas ke penghancur diri atau media.**
"""
