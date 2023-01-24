import asyncio
from time import time
from typing import List
from Darmiubot import *
from pyrogram import Client
from pyrogram.types import Message, Chat, User
from Darmiubot.modules.helpers.interval import IntervalHelper
import Darmiubot.modules.cache.admins

async def get_administrators(chat: Chat) -> List[User]:
    get = Darmiubot.modules.cache.admins.get(chat.id)

    if get:
        return get
    else:
        administrators = await chat.get_members(filter="administrators")
        to_set = []

        for administrator in administrators:
            if administrator.can_manage_voice_chats:
                to_set.append(administrator.user.id)

        Darmiubot.modules.cache.admins.set(chat.id, to_set)
        return await get_administrators(chat)



async def CheckAdmin(client: Client, message: Message):
    """Periksa apakah kita seorang admin."""
    admin = "administrator"
    creator = "creator"
    ranks = [admin, creator]

    SELF = await client.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )

    if SELF.status not in ranks:
        await message.edit("__Saya bukan Admin!__")
        await asyncio.sleep(2)
        await message.delete()

    else:
        if SELF.status is not admin:
            return True
        elif SELF.can_restrict_members:
            return True
        else:
            await message.edit("__Tidak Ada Izin untuk membatasi Anggota__")
            await asyncio.sleep(2)
            await message.delete()


async def CheckReplyAdmin(message: Message):
    """Periksa apakah pesan tersebut merupakan balasan ke pengguna lain."""
    if not message.reply_to_message:
        await message.edit("Perintah harus berupa balasan")
        await asyncio.sleep(2)
        await message.delete()
    elif message.reply_to_message.from_user.is_self:
        await message.edit(f"Saya tidak bisa {message.command[0]} saya sendiri.")
        await asyncio.sleep(2)
        await message.delete()
    else:
        return True

    return False


async def Timer(message: Message):
    if len(message.command) > 1:
        secs = IntervalHelper(message.command[1])
        return int(str(time()).split(".")[0] + secs.to_secs()[0])
    else:
        return 0


async def TimerString(message: Message):
    secs = IntervalHelper(message.command[1])
    return f"{secs.to_secs()[1]} {secs.to_secs()[2]}"


async def RestrictFailed(message: Message):
    await message.edit(f"Saya tidak bisa {message.command} pengguna ini.")
    await asyncio.sleep(2)
    await message.delete()
