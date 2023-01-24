import requests
from datetime import datetime
from pyrogram import filters, Client
from Darmiubot.utilities.misc import SUDOERS
# ping checker

@Client.on_message(filters.command(["ping"], ["/", ".", "!"]) & SUDOERS)
async def ping(Client, message):
    start = datetime.now()
    loda = await message.reply_text("**Darmiubot**")
    end = datetime.now()
    mp = (end - start).microseconds / 1000
    await loda.edit_text(f"**🤖 Poɴɢ\n»** `{mp} ms`")


__MODULE__ = "Pɪɴɢ"
__HELP__ = f"""
**Cek ping Darmi bot.**

`.ping` - **Gunakan perintah ini untuk ngecek**
"""
