import os
import shutil
import asyncio
from git import Repo
from pyrogram.types import Message
from pyrogram import filters, Client
from git.exc import GitCommandError, InvalidGitRepositoryError
from Darmiubot.modules.helpers.basics import edit_or_reply
from Darmiubot.modules.helpers.filters import command
from Darmiubot.utilities.misc import SUDOERS


@Client.on_message(command(["restart", "reboot"]) & filters.me)
async def restart(client, m: Message):
    reply = await m.edit("**ð Merestart ð¥ ...**")
    
    await reply.edit(
        "Restar Sukses\nDarmi ã·ï¸ Userbot ð¥ ...\n\nð Tolong tunggu 1-2 menit untuk\nmemuat plagin pengguna â¨ ...</b>"
    )
    os.system(f"kill -9 {os.getpid()} && python3 -m modules")





__MODULE__ = "Rá´sá´á´Êá´"
__HELP__ = f"""
`.restart` **- Gunakan command ini untuk merestart Darmi bot**

"""
