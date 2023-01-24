import asyncio
from pyrogram import Client, filters 
from pyrogram.types import Message
from Darmiubot.modules.helpers.basics import edit_or_reply
from Darmiubot.modules.helpers.filters import command
from Darmiubot.modules.helpers.command import commandpro
from Darmiubot.utilities.misc import SUDOERS


@Client.on_message(command(["culik", "culikm"]) & SUDOERS)
async def inviteall(client: Client, message: Message):
    kaal = await edit_or_reply(message, "Memproses culik member ...")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await kaal.edit_text(f"** Culik member dari {chat.username} ...**")
    async for member in client.iter_chat_members(chat.id):
        user= member.user
        kal = ["online", "offline" , "baru-baru ini", "dalam_minggu"]
        if user.status in kal:
            try:
            await client.add_chat_members(tgchat.id, user.id)
            except Exception as e:
            mg = await client.send_message("me", f"error-   {e}")
            await asyncio.sleep(0.3)
            await mg.delete()



__MODULE__ = "Culik Member"
__HELP__ = f"""
`.culik [@groupusername]` **- Gunakan ini untuk culik member**

**Contoh :-** `.culik @kuyjugi`
"""
