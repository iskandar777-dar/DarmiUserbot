from pyrogram import filters
from pyrogram.types import Message

from Darmiubot.config import MONGO_DB_URL, OWNER_ID

from Darmiubot.modules.clientbot.clientbot import client as app
from Darmiubot.modules.helpers.command import commandpro
from Darmiubot.utilities.misc import SUDOERS
from Darmiubot.utilities.utils import add_sudo, remove_sudo



@app.on_message(
    commandpro([".addsudo"]) & filters.user(OWNER_ID)
)
async def useradd(client, message: Message):
    if MONGO_DB_URL is None:
        return await message.reply_text(
            "**Karena masalah privasi bot, Anda tidak dapat mengelola pengguna sudo saat menggunakan Basis Data Yukki.\n\n Silakan isi MONGO_DB_URI Anda di vars untuk menggunakan fitur ini**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("Balas pesan pengguna atau berikan nama pengguna/id_pengguna.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                "{0} sudah menjadi pengguna sudo.".format(user.mention)
            )
        added = await add_sudo(user.id)
        if added:
            SUDOERS.add(user.id)
            await message.reply_text("Menambahkan **{0}** ke Pengguna Sudo.".format(user.mention))
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            "{0} sudah menjadi pengguna sudo.".format(
                message.reply_to_message.from_user.mention
            )
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        SUDOERS.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            "Menambahkan **{0}** ke Pengguna Sudo.".format(
                message.reply_to_message.from_user.mention
            )
        )
    else:
        await message.reply_text("Gagal")
    return


@app.on_message(
    commandpro([".delsudo"]) & filters.user(OWNER_ID)
)
async def userdel(client, message: Message):
    if MONGO_DB_URL is None:
        return await message.reply_text(
            "**Karena masalah privasi bot, Anda tidak dapat mengelola pengguna sudo saat menggunakan Basis Data Yukki.\n\n Silakan isi MONGO_DB_URI Anda di vars untuk menggunakan fitur ini**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("Balas pesan pengguna atau berikan nama pengguna/id_pengguna.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in SUDOERS:
            return await message.reply_text("Bukan bagian dari Sudo Bot.")
        removed = await remove_sudo(user.id)
        if removed:
            SUDOERS.remove(user.id)
            await message.reply_text("Dihapus dari Pengguna Sudo Bot")
            return
        await message.reply_text(f"Sesuatu yang salah terjadi.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in SUDOERS:
        return await message.reply_text("Bukan bagian dari Sudo Bot.")
    removed = await remove_sudo(user_id)
    if removed:
        SUDOERS.remove(user_id)
        await message.reply_text("Dihapus dari Pengguna Sudo Bot")
        return
    await message.reply_text(f"Sesuatu yang salah terjadi.")


@app.on_message(commandpro([".sudousers", ".sudolist"]) & SUDOERS)
async def sudoers_list(client, message: Message):
    text = "⭐️<u> **Pemilik :**</u>\n"
    count = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = (
                user.first_name if not user.mention else user.mention
            )
            count += 1
        except Exception:
            continue
        text += f"{count}➤ {user}\n"
    smex = 0
    for user_id in SUDOERS:
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = (
                    user.first_name
                    if not user.mention
                    else user.mention
                )
                if smex == 0:
                    smex += 1
                    text += "\n⭐️<u> **Pemilik Sude:**</u>\n"
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("Bukan Pemilik Sude")
    else:
        await message.reply_text(text)



__MODULE__ = "Sᴜᴅᴏ"
__HELP__ = f"""
**Pengguna Sudo kontrol :**

`.addsudo` - **Menambahkan Pengguna Sudo**

`.delsudo` - **Melepaskan Pengguna Sudo**

`.sudolist` - **Menampilkan list Pengguna Sudo**
"""
