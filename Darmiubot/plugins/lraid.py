# Kang With Credit » @Darmiubot

import random
from typing import Tuple
from pyrogram import Client
from pyrogram import filters
from traceback import format_exc
from Darmiubot.utilities.data import *
from Darmiubot.modules.helpers.filters import command
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import (
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message)
from Darmiubot.utilities.mongo import loveub_info, rlove, runlove
from Darmiubot.modules.helpers.decorators import errors, sudo_users_only
from Darmiubot.utilities.misc import SUDOERS


async def iter_chats(client: Client):
    """Iter Semua Obrolan Anda"""
    chats = []
    async for dialog in client.iter_dialogs():
        if dialog.chat.type in ["supergroup", "channel"]:
            chats.append(dialog.chat.id)
    return chats

def get_user(message: Message, text: str) -> [int, str, None]:
    """Dapatkan Pengguna Dari Pesan"""
    if text is None:
        asplit = None
    else:
        asplit = text.split(" ", 1)
    user_s = None
    reason_ = None
    if message.reply_to_message:
        user_s = message.reply_to_message.from_user.id
        reason_ = text if text else None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        if message.entities:
            if len(message.entities) == 1:
                required_entity = message.entities[0]
                if required_entity.type == "text_mention":
                    user_s = int(required_entity.user.id)
                else:
                    user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        else:
            user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


async def edit_or_send_as_file(
    text: str,
    message: Message,
    client: Client,
    caption: str = "`Result!`",
    file_name: str = "result",
    parse_mode="md",
):
    """Kirim Sebagai File Jika Len Teks Melebihi Tg Batas Lain Edit Pesan"""
    if not text:
        await message.edit("`Tunggu, apa?`")
        return
    if len(text) > 1024:
        await message.edit("`Keluaran Terlalu Besar, Dikirim Sebagai File!`")
        file_names = f"{file_name}.text"
        open(file_names, "w").write(text)
        await client.send_document(message.chat.id, file_names, caption=caption)
        await message.delete()
        if os.path.exists(file_names):
            os.remove(file_names)
        return
    else:
        return await message.edit(text, parse_mode=parse_mode)

def get_text(message: Message) -> [None, str]:
    """Ekstrak Teks Dari Perintah"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

   


@Client.on_message(command(["loveraid", "lraid", "lr"]) & SUDOERS)
async def replyramd(client: Client, message: Message):
    await message.delete()
    Kaal = await message.reply_text("`Memproses..`")
    text_ = get_text(message)
    user, reason = get_user(message, text_)
    failed = 0
    if not user:
        await Kaal.edit("`Balas Ke Pengguna Atau Sebutkan Untuk Mengaktifkan LoveRaid `")
        return
    try:
        userz = await client.get_users(user)
    except:
        await Kaal.edit(f"`404 : Pengguna Tidak Ada Dalam Obrolan Ini !`")
        return
    if not reason:
        reason = "Alasan Pribadi!"
    mee= await client.get_me()
    if userz.id == mee.id:
        await Kaal.edit("`Darmi Ubot saikho?`")
        return
    if await loveub_info(userz.id):
        await Kaal.edit("`Siapa Jadi Noob? LoveRaid Sudah Diaktifkan pada Pengguna tersebut:/`")
        return
    await Kaal.edit("`Tolong, Tunggu Mengambil Menggunakan Detail!`")
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        Kaal.edit("`Anda Tidak Memiliki Obrolan! Sangat sedih`")
        return
    await Kaal.edit("`Mengaktifkan LoveRaid....!`")
    await rlove(userz.id, reason)
    gbanned = f"LoveRaid Telah Diaktifkan Pada {userz.first_name}"
    await Kaal.edit(gbanned)
    

@Client.on_message(command(["dloveraid", "dlraid", "dlr"]) & SUDOERS)
async def dreplyramd(client: Client, message: Message):
    await message.delete()
    Kaal = await message.reply_text("`Memproses..`")
    text_ = get_text(message)
    user = get_user(message, text_)[0]
    failed = 0
    if not user:
        await Kaal.edit("`Balas Ke Pengguna Atau Sebutkan Untuk Menonaktifkan LoveRaid`")
        return
    try:
        userz = await client.get_users(user)
    except:
        await Kaal.edit(f"`404 : Pengguna Tidak Ada!`")
        return
    mee= await client.get_me()
    if userz.id == mee.id:
        await Kaal.edit("`Dami ubot`")
        return
    if not await loveub_info(userz.id):
        await Kaal.edit("`Soja TharkKapan Saya Menyukai Raid Diaktifkan? Pada Pengguna Itu?:/`")
        return
    await Kaal.edit("`Tolong, Tunggu Menjemput detail Pengguna!`")
    chat_dict = await iter_chats(client)
    chat_len = len(chat_dict)
    if not chat_dict:
        Kaal.edit("`Anda Tidak Memiliki Obrolan! Sangat sedih`")
        return
    await Kaal.edit("`Menonaktifkan Serangan LoveRaid....!`")
    await runlove(userz.id)
    ungbanned = f"**Serangan LoveRaid yang dinonaktifkan [{userz.first_name}](tg://user?id={userz.id})"
    await Kaal.edit(ungbanned)

