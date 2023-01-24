import asyncio
from pyrogram import *
from pyrogram.types import *
from Darmiubot.modules.helpers.basics import edit_or_reply
from Darmiubot.modules.helpers.command import commandpro
from Darmiubot.utilities.misc import SUDOERS


MOTIV = "Seberat apapun masalahmu, bukan masalahku!!"



@Client.on_message(commandpro(["motivasi"]) & SUDOERS)
async def mother_chod(client: Client, message: Message):
    kaal = await edit_or_reply(message, "Motivasi ...")
    await asyncio.sleep(2)
    await kaal.edit(MOTIV)
    
    
__MODULE__ = "motivasi"
__HELP__ = f"""
** Motivasi Darmi **

**Cᴏᴍᴍᴀɴᴅs:**

`motivasi` - **Balas Pesan untuk memberikan motivasi**
"""
