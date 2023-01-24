import asyncio
from pyrogram import filters, Client
from pyrogram.methods import messages
from Darmiubot.modules.helpers.filters import command
from Darmiubot.modules.helpers.program import get_arg, denied_users
import Darmiubot.modules.databases.pmpermit_db as Kaal

FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}


@Client.on_message(command(["pmguard", "antipm"]) & filters.me)
async def antipm(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Saya hanya mengerti hidup atau mati**")
        return
    if arg == "off":
        await Kaal.set_pm(False)
        await message.edit("**Penjaga PM Dinonaktifkan**")
    if arg == "on":
        await Kaal.set_pm(True)
        await message.edit("**Penjaga PM Diaktifkan**")




@Client.on_message(command("setlimit") & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Tetapkan batas untuk apa?**")
        return
    await Kaal.set_limit(int(arg))
    await message.edit(f"**Batas ditetapkan ke {arg}**")


@Client.on_message(command("setpmmsg") & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Pesan apa yang harus ditetapkan**")
        return
    if arg == "default":
        await Kaal.set_permit_message(Kaal.PMPERMIT_MESSAGE)
        await message.edit("**Pesan anti_PM disetel ke default**.")
        return
    await Kaal.set_permit_message(f"`{arg}`")
    await message.edit("**Kumpulan pesan anti-pm khusus**")


@Client.on_message(command("setblockmsg") & filters.me)
async def setblkmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Pesan apa yang harus ditetapkan**")
        return
    if arg == "default":
        await Kaal.set_block_message(Kaal.BLOCKED)
        await message.edit("**Blokir pesan disetel ke default**.")
        return
    await Kaal.set_block_message(f"`{arg}`")
    await message.edit("**Kumpulan pesan blokir khusus**")


@Client.on_message(command(["allow", "ap", "approve", "a"]) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    pmpermit, pm_message, limit, block_message = await Kaal.get_pm_settings()
    await Kaal.allow_user(chat_id)
    await message.edit(f"**Saya telah mengizinkan [kamu](tg://user?id={chat_id}) untuk PM saya.**")
    async for message in app.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS.update({chat_id: 0})


@Client.on_message(command(["deny", "da", "dap", "disapprove", "dapp"]) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    await Kaal.deny_user(chat_id)
    await message.edit(f"**Saya telah menyangkal [kamu](tg://user?id={chat_id}) untuk PM saya.**")


@Client.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def reply_pm(app: Client, message):
    global FLOOD_CTRL
    pmpermit, pm_message, limit, block_message = await Kaal.get_pm_settings()
    user = message.from_user.id
    user_warns = 0 if user not in USERS_AND_WARNS else USERS_AND_WARNS[user]
    if user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        async for message in app.search_messages(
            chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
        ):
            await message.delete()
        await message.reply(pm_message, disable_web_page_preview=True)
        return
    await message.reply(block_message, disable_web_page_preview=True)
    await app.block_user(message.chat.id)
    USERS_AND_WARNS.update({user: 0})




__MODULE__ = "Anti PM"
__HELP__ = f""" Modul ini hanya untuk pemilik

`.pmguard [aktif atau nonaktif]` - Menghidupkan atau Mematikan Aɴᴛɪ-Pᴍ

`.setpmmsg [pesan atau default]` - Menset pesan Pm

`.setblockmsg [pesan atau default]` - Menset pesan Blok

`.setlimit [nilai]` - Menset maksimum limit pesan.
Contoh:- `.setlimit 3` [Nilai Tetap - 5]

`.a/.allow` - Menerima pesan.

`.da/.deny` - Menolak pesan.

**ɴᴏᴛᴇ:**
- Pengguna sudo tidak bisa menggunakan plugin ini
"""
