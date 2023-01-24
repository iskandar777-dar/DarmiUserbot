import asyncio
from pyrogram import *
from pyrogram import filters
from pyrogram.types import *
from pyrogram.errors import RPCError
from Darmiubot.modules.helpers.basics import edit_or_reply
from Darmiubot.modules.helpers.filters import command
from Darmiubot.modules.helpers.command import commandpro
from Darmiubot.modules.helpers.decorators import sudo_users_only, errors
from Darmiubot.utilities.misc import SUDOERS



@Client.on_message(command(["history"]) & SUDOERS)
async def user_history(client: Client, message: Message):
    lol = await edit_or_reply(message, "Memproses ... tunggu sebentar")
    if not message.reply_to_message:
        await lol.edit("membalas pesan apapun")
    reply = message.reply_to_message
    if not reply.text:
        await lol.edit("membalas pesan teks apa pun")
    chat = message.chat.id
    try:
        await client.send_message("@SangMataInfo_bot", "/start")
    except RPCError:
        await lol.edit("Buka blokir @SangMataInfo_bot dan coba lagi")
        return
    await reply.forward("@SangMataInfo_bot")
    await asyncio.sleep(2)
    async for opt in client.iter_history("@SangMataInfo_bot", limit=3):
        hmm = opt.text
        if hmm.startswith("Forward"):
            await lol.edit("Bisakah Anda menonaktifkan pengaturan privasi Anda untuk selamanya")
            return
        else:
            await lol.delete()
            await opt.copy(chat)



__MODULE__ = "Hɪsᴛᴏʀʏ"
__HELP__ = f"""
**Mendapatkan Sejarah Nama dan Username Pengguna**

**Penggunaan :**
`.history` - **Balas ke pesan pengguna.**
"""
