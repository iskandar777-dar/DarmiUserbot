import asyncio
import importlib
import os
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pytgcalls import idle
from rich.console import Console
from rich.table import Table
from youtubesearchpython import VideosSearch

from Darmiubot.config import LOG_GROUP_ID, STRING_SESSION
from Darmiubot import client, robot, pytgcalls, ASSID, ASSNAME, BOT_ID, BOT_NAME, OWNER_ID
from Darmiubot.modules.helpers.filters import command
from Darmiubot.modules.helpers.decorators import errors, sudo_users_only
from Darmiubot.plugins import ALL_MODULES
from Darmiubot.utilities.inline import paginate_modules
from Darmiubot.utilities.misc import SUDOERS

loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}


async def initiate_bot():
    with console.status(
        "[magenta] Menyelesaikan Booting...",
    ) as status:
        status.update(
            status="[bold blue]Memindai Plugin", spinner="earth"
        )
        console.print("Ditemukan {} Plugin".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Mengimpor Plugin...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "Darmiubot.plugins." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f">> [bold cyan]Berhasil diimpor: [green]{all_module}.py"
            )
        console.print("")
        status.update(
            status="[bold blue]Impor Selesai!",
        )
    console.print(
        "[bold green] Darmi Userbot Dimulai ✨\n"
    )
    try:
        await robot.send_message(
            LOG_GROUP_ID,
            "<b> Darmi UserBot Disini ✨</b>",
        )
    except Exception as e:
        print(
            "\nBot. Gagal Mengakses Grup Log, Pastikan Anda Telah Menambahkan Bot Anda ke Saluran Log Anda Dan Dipromosikan Sebagai Admin❗"
        )
        console.print(f"\n[red] Menghentikan Bot")
        return
    a = await robot.get_chat_member(LOG_GROUP_ID, BOT_ID)
    if a.status != "administrator":
        print("Promosikan Bot Sebagai Admin di Grup Logger")
        console.print(f"\n[red]Memberhentikan ʙᴏᴛ")
        return
    console.print(f"\n┌[red] Bot Dimulai Sebagai {BOT_NAME}")
    console.print(f"├[green] ID :- {BOT_ID}")
    if STRING_SESSION != "None":
        try:
            await client.send_message(
                LOG_GROUP_ID,
                "<b>Darmi UserBot Aktif ✨</b>",
            )
        except Exception as e:
            print(
                "\nAkun UserBot Gagal Mengakses Grup Log.❗"
            )
            console.print(f"\n[red] Menghentikan Bot")
            return
        try:
            await client.join_chat("medsupportt")
            await client.join_chat("medchannell")
        except:
            pass
        console.print(f"├[red] UserBot Dimulai sebagai {ASSNAME}")
        console.print(f"├[green] ID :- {ASSID}")
        console.print(f"└[red] ✅ Boot Darmi UserBot Selesai 💯 ...")
        await idle()
        console.print(f"\n[red] Userbot Dihentikan")


home_text_pm = f"""**ʜᴇʟʟᴏ ,
Nama saya adalah {BOT_NAME}.
Aku Adalah Userbot dengan banyak fitur.**"""


@robot.on_message(command(["start"]) & filters.private)
async def start(_, message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/c8f5100f93070495ba75b.png",
        caption=f"""**━━━━━━━━━━━━━━━━━━━━━━━━
💥 Hai, Saya Darmi » Premium Userbot Telegram.

┏━━━━━━━━━━━━━━━━━━━┓
┣★ Oᴡɴᴇʀ'xD› : [Damri Hᴀʟᴅᴇʀ](https://t.me/Kenapatagdar)
┣★ Uᴘᴅᴀᴛᴇs ›› : [Damri Sᴇʀᴠᴇʀ](https://t.me/medsuportt)
┣★ Sᴜᴘᴘᴏʀᴛ » : [Damri Dɪsᴄᴜs](https://t.me/medchannell)
┗━━━━━━━━━━━━━━━━━━━┛

Klik tombol deploy untuk membuat
Darmi userbot.
━━━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💥 Deploy Darmi Userbot ✨", url=f"https://github.com/iskandar777-dar/Darmiubot")
                ]
                
           ]
        ),
    )
    
    
    
@robot.on_message(command(["help"]) & SUDOERS)
async def help_command(_, message):
    text, keyboard = await help_parser(message.from_user.mention)
    await robot.send_message(LOG_GROUP_ID, text, reply_markup=keyboard)




async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """**Selamat Datang Dibot Menu :
DarmiUerbot 🔥...

Hanya klik dibawah saja untuk melihat 
Perintah Darmi✨...**
""".format(
            first_name=name
        ),
        keyboard,
    )

@robot.on_callback_query(filters.regex("close") & SUDOERS)
async def close(_, CallbackQuery):
    await CallbackQuery.message.delete()

@robot.on_callback_query(filters.regex("aditya") & SUDOERS)
async def aditya(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@robot.on_callback_query(filters.regex(r"help_(.*?)") & SUDOERS)
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""**Selamat Datang Dibot Menu :
DarmiUerbot 🔥...

Hanya klik dibawah saja untuk melihat 
Perintah Darmi✨...**
"""
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "** Selamat datang dimenu untuk :** ", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Kembali", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="🔄 Menutup", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    elif home_match:
        out = private_panel()
        await robot.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    loop.run_until_complete(initiate_bot())
