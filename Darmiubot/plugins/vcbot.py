# 𝐊𝐚𝐚𝐥 𝐌𝐮𝐬𝐢𝐜 // @𝐢𝐚𝐦𝐤𝐚𝐚𝐥

import os
import sys
import json
import time
import aiofiles
import aiohttp
import ffmpeg
import requests
from os import path
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from Darmiubot.modules.cache.admins import set
from Darmiubot.modules.clientbot import clientbot, queues
from Darmiubot.modules.clientbot.clientbot import client as USER
from Darmiubot.modules.helpers.admins import get_administrators
from Darmiubot.modules import converter
from Darmiubot.modules.downloaders import youtube
from Darmiubot.config import que
from Darmiubot.modules.cache.admins import admins as a
from Darmiubot.modules.helpers.command import commandpro
from Darmiubot.modules.helpers.filters import command, other_filters
from Darmiubot.modules.helpers.decorators import SUDO_USERS, errors, sudo_users_only
from Darmiubot.modules.helpers.errors import DurationLimitError
from Darmiubot.modules.helpers.gets import get_url, get_file_name
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.exceptions import GroupCallNotFound, NoActiveGroupCall
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from Darmiubot.utilities.misc import SUDOERS
# plus
chat_id = None
useer = "NaN"


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))



@Client.on_message(
    commandpro([".ply", "ply"]) & SUDOERS)
async def play(_, message: Message):
    global que
    global useer
    await message.delete()
    lel = await message.reply("**🔄 Memproses ...**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id


    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/513c2e33e8da59482674b.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Ditambahkan secara lokal"


        requested_by = message.from_user.first_name
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/513c2e33e8da59482674b.png"
            duration = "NaN"
            views = "NaN"

        requested_by = message.from_user.first_name
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
           return await lel.edit(
                "**🤖 Apa yang mau diputar ❓**"
            ) and await lel.delete()

        await lel.edit("**🔎 Mencari ...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("**✅ Menyelesaikan ...**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**🔊 Musik Tidak Ditemukan❗️,\nMencoba Yang Lain...**"
            ) and await lel.delete()
            print(str(e))
            return


        requested_by = message.from_user.first_name
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await lel.edit("**💥 Darmi Menambahkan 💿 Laku❗️\nDi Posisi » `{}`...**".format(position),
    )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await lel.edit("**💥 Darmi \nMemulai Lagu 🎸...**".format(),
        )

    return await lel.delete()
    
    
    
@Client.on_message(commandpro([".pse", "pse"]) & SUDOERS)
async def pause(_, message: Message):
    await message.delete()
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        noac = await message.reply_text("**💥 Tidak Ada Yang Diputar ...**")
        await noac.delete()
    else:
        await clientbot.pytgcalls.pause_stream(message.chat.id)
        pase = await message.reply_text("**▶️ Memberhentikan ...**")
        await pase.delete()

@Client.on_message(commandpro([".rsm", "rsm"]) & SUDOERS)
async def resume(_, message: Message):
    await message.delete()
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        noac = await message.reply_text("**💥 Tidak Ada Yang Diputar ...**")
        await noac.delete()
    else:
        await clientbot.pytgcalls.resume_stream(message.chat.id)
        rsum = await message.reply_text("**⏸ Meneruskan Kembali ...**")
        await rsum.delete()


@Client.on_message(commandpro([".skp", "skp"]) & SUDOERS)
async def skip(_, message: Message):
    global que
    await message.delete()
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
       novc = await message.reply_text("**💥 Tidak ada yang Diputar ...**")
       await novc.delete()
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            empt = await message.reply_text("**antrian kosong, meninggalkan vc ✨ ...**")
            await empt.delete()
            await clientbot.pytgcalls.leave_group_call(chat_id)
        else:
            next = await message.reply_text("**⏩ dilewati ...**")
            await next.delete()
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )
             


@Client.on_message(commandpro([".stp", ".end", "end", "stp"]) & SUDOERS)
async def stop(_, message: Message):
    await message.delete()
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        noac = await message.reply_text("**💥 Tidak ada yang diputar ...**")
        await noac.delete()
        return
    else:
        try:
            clientbot.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    leav = await message.reply_text("**❌ Memberhentikan ...**")
    await leav.delete()


@Client.on_message(commandpro([".song", "sng", ".sng", ".msc", "msc"]) & SUDOERS)
async def song(client, message):
    cap = "**Diunggah oleh ː [Tuan'Darmi](https://t.me/kenapatagdar)**"
    rkp = await message.reply("**🔄 Memproses ...**")

    if len(message.command) < 2:
            return await rkp.edit(
                "**Berikan Judul Lagu ...**"
            )
    url = message.text.split(None, 1)[1]
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("**lagu Tidak Ditemukan ...**")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("**📩 Mendownload ...**")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`Konten unduhan terlalu singkat.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video tidak tersedia dari lokasi geografis Anda karena batasan geografis yang diberlakukan oleh situs web.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Batas unduhan maksimum telah tercapai.`")
        return
    except PostProcessingError:
        await rkp.edit("`Terjadi kesalahan selama pemrosesan pos.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media tidak tersedia dalam format yang diminta.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`Terjadi kesalahan selama ekstraksi info.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("**📤 mengunggah ...**")
        lol = "./Darmiubot/resource/logo.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["durasi"]),
                 title=str(rip_data["judul"]),
                 performer=str(rip_data["pengunggah"]),
                 thumb=lol,
                 caption=cap) 
        await rkp.delete()


@Client.on_message(commandpro([".rld", "rld"]) & SUDOERS)
async def update_admin(client, message):
    global a
    await message.delete()
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    a[message.chat.id] = new_admins
    cach = await message.reply_text("**dimuat ulang ...**")
    await cach.delete()


__MODULE__ = "Vc Bot"
__HELP__ = f"""
**Kamu bisa putar lagu divc**

`.ply` - Memulai musik
`.pse` - Memberhentikan sementara musik
`.rsm` - Melanjutkan Musik
`.skp` - Melewti musik
`.stp` - Memberhentikan musik dan keluar vc
`.sng` - Mendownload lagu
`.rld` - Memuat Ulang
"""
