# AdityaHalder
import asyncio
from pyrogram import *
from pyrogram.types import *
from Darmiubot.modules.helpers.basics import edit_or_reply
from Darmiubot.modules.helpers.filters import command
from Darmiubot.utilities.misc import SUDOERS


@Client.on_message(command(["hidup"]) & SUDOERS)
async def mother_chod(client: Client, message: Message):
    await edit_or_reply(message, "**Saya Hidup Tuan ...**")



__MODULE__ = "Hidup"
__HELP__ = f"""
**Mengetes apakah bot hidup atau tidak.**

`.hidup` - **Gunakan untuk mengecek bot**
"""
