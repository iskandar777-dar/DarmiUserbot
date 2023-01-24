import sys
from git import Repo
from os import system, execle, environ
from git.exc import InvalidGitRepositoryError
from pyrogram.types import Message
from pyrogram import filters, Client
from Darmiubot.config import UPSTREAM_REPO, UPSTREAM_BRANCH, OWNER_ID
from Darmiubot.modules.helpers.filters import command


def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = ""
    tldr_log = ""
    ch = f"<b>Pembaruan untuk <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"Pembaruan untuk {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n\n💬 <b>{c.count()}</b> 🗓 <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b>"
            f"<a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> 👨‍💻 <code>{c.author}</code>"
        )
        tldr_log += f"\n\n💬 {c.count()} 🗓 [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] 👨‍💻 {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head("UPSTREAM_BRANCH", origin.refs.UPSTREAM_BRANCH)
        repo.heads.UPSTREAM_BRANCH.set_tracking_branch(origin.refs.UPSTREAM_BRANCH)
        repo.heads.UPSTREAM_BRANCH.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM_REPO)
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


@Client.on_message(command(["update"]) & filters.user(OWNER_ID) & ~filters.edited)
async def update_bot(_, message: Message):
    chat_id = message.chat.id
    msg = await message.edit("**Mengecek Update ...**")
    update_avail = updater()
    if update_avail:
        await msg.edit("**Pembaruan Darmi Userbot\nuntuk versi terbaru 🔥 ...\n\nMerestart : Darmi User\nBot, Tolong » Tunggu...**")
        system("git pull -f && pip3 install -U -r Installer")
        system("python3 -m Darmiubot")
        return
    await msg.edit(f"**Darmi Userbot Berhasil Diupdate\nKe versi terbaru 🔥 ...\n\nUntuk kueri apa pun › Kontak \nKe » @kenapatagdar ...**")

__MODULE__ = "Pembaruan"
__HELP__ = f"""

**Catatn :**
**Plagin ini Untuk Pembaruan**

**Perintah :**
`.update` - __Untuk Update Darmi Userbot...__
"""
