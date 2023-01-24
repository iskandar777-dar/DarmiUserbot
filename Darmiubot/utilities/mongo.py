# Aditya Halder // @AdityaHalder
from Darmiubot.utilities import dbb

Rbun = dbb["RBAN"]


async def rkaal(user, reason="#MATHERCHOD"):
    await Rbun.insert_one({"Pengguna": user, "Alasan": reason})


async def runkaal(user):
    await Rbun.delete_one({"Pengguna": user})


async def rban_list():
    return [lo async for lo in Rbun.find({})]


async def kaalub_info(user):
    kk = await Rbun.find_one({"Pengguna": user})
    if not kk:
        return False
    else:
        return kk["Alasan"]


# Aditya Halder // @AdityaHalder

Lbun = dbb["LBAN"]


async def rlove(user, reason="#MYLOVER"):
    await Lbun.insert_one({"Pengguna": user, "Alasan": reason})


async def runlove(user):
    await Lbun.delete_one({"Pengguna": user})


async def lban_list():
    return [lo async for lo in Lbun.find({})]


async def loveub_info(user):
    um = await Lbun.find_one({"Pengguna": user})
    if not um:
        return False
    else:
        return um["Alasan"]
