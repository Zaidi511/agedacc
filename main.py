import asyncio
import uuid
import random
import string
import requests
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import ForwardMessagesRequest
from telethon.tl.types import PeerChannel

# --------------- CONFIG ------------------
API_ID      = 20225326
API_HASH    = '549070bf022402aec24ce667b867af8f'
BOT_TOKEN   = '7783929609:AAFgBKvx9Mxovu291-yDQlQsyEqrc7Aa8o0'
SESSION     = 'session'
INTERVAL    = 60 * 60  # seconds

# --------------- EMBEDDED GROUPS ----------
links = [
    "https://t.me/thedealmarket/11237",
    "https://t.me/ghostly2/1554",
    "https://t.me/celismarket/8266",
    "https://t.me/sectormarket/24",
    "https://t.me/c/2256623070/11992",
    "https://t.me/stockless/39",
    "https://t.me/MediaPlugs/6",
    "https://t.me/TheStockChat/245496",
    "https://t.me/saving",
    "https://t.me/oguflip/11204",
    "https://t.me/buffestmarket/20",
    "https://t.me/StateMarkets/319",
    "https://t.me/thedealmarket/11237",
    "https://t.me/aizenmarket/21",
    "https://t.me/deciomrkt",
    "https://t.me/escrrowonces2",
    "https://t.me/emarket/224",
    "https://t.me/EscrowpIace/21",
    "https://t.me/RareHandle/79",
    "https://t.me/OFMrevolution",
    "https://t.me/OFMgrind",
    "https://t.me/jezzy_market",
    "https://t.me/ofmserviceswork",
    "https://t.me/pinkvibescommunity",
    "https://t.me/voffofm",
    "https://t.me/ofmjoino",
    "https://t.me/redditofmgroup",
    "https://t.me/ofmadvault",
    "https://t.me/OFMPromote",
    "https://t.me/ofmmonopoly",
    "https://t.me/theofmfirm",
    "https://t.me/ofmboardj",
    "https://t.me/ofmjoin",
    "https://t.me/S4SandPromo",
    "https://t.me/OFMManiacs",
    "https://t.me/OFMTheHub/3191",
    "https://t.me/ofmtrade",
    "https://t.me/redditjobs",
    "https://t.me/OFMResurgehub",
    "https://t.me/zazazamkx",
    "https://t.me/orbisgroup2",
    "https://t.me/OnlyFansFuture",
    "https://t.me/OFforum/8",
    "https://t.me/IGMarket2024",
    "https://t.me/FVMJobs",
    "https://t.me/bunnyfap_chat",
    "https://t.me/ofmelites",
    "https://t.me/HauteClubOFM",
    "https://t.me/marketOFM",
    "https://t.me/onlyfansdropsfreepaid",
    "https://t.me/texted/24",
    "https://t.me/SocialCove/3",
    "https://t.me/blackmarket/227701",
    "https://t.me/GooMarketplace/14577",
    "https://t.me/DicesMarket/15",
    "https://t.me/OFMGroundFloor",
    "https://t.me/OFMJobs",
    "https://t.me/OnlyForOfm",
    "https://t.me/PrimeClubOFM",
    "https://t.me/RoubleMarket/1416",
    "https://t.me/contrlofm/1805",
    "https://t.me/errormystry/94",
    "https://t.me/fanzellachat",
    "https://t.me/kimsocialMP/2",
    "https://t.me/ofmpinboard",
    "https://t.me/ofmrealmxMM",
    "https://t.me/vaofm",
    "https://t.me/whalesofmjobs"
]

# --------------- TELETHON -----------------
tel_client = TelegramClient(SESSION, API_ID, API_HASH)

# --------------- AIROGRAM -----------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
last_message = None

# --------------- FORWARD LOOP -------------
async def forward_messages():
    global last_message
    await tel_client.start()
    print("â Forwarding loop started")

    while True:
        try:
            msgs = await tel_client.get_messages('me', limit=1)
            if not msgs:
                await asyncio.sleep(INTERVAL)
                continue

            last_message = msgs[0]
            success_count = 0
            error_count = 0

            for link in links:
                try:
                    if '/c/' in link:
                        chan, topic = link.split('/c/')[1].split('/', 1)
                        peer = PeerChannel(int(chan))
                        await tel_client(ForwardMessagesRequest(
                            from_peer='me',
                            id=[last_message.id],
                            to_peer=peer,
                            top_msg_id=int(topic)
                        ))
                    elif '/' in link.replace('https://t.me/', ''):
                        name, topic = link.replace('https://t.me/', '').split('/', 1)
                        ent = await tel_client.get_entity(name)
                        await tel_client(ForwardMessagesRequest(
                            from_peer='me',
                            id=[last_message.id],
                            to_peer=ent,
                            top_msg_id=int(topic)
                        ))
                    else:
                        name = link.replace('https://t.me/', '')
                        ent = await tel_client.get_entity(name)
                        await tel_client(ForwardMessagesRequest(
                            from_peer='me',
                            id=[last_message.id],
                            to_peer=ent
                        ))

                    success_count += 1

                except FloodWaitError as e:
                    print(f"â³ Flood wait {e.seconds}s")
                    await asyncio.sleep(e.seconds)
                    error_count += 1
                except Exception as e:
                    print(f"â Error: {e}")
                    error_count += 1

            print(f"â Sent: {success_count} | â Errors: {error_count}")
            await asyncio.sleep(INTERVAL)

        except Exception as e:
            print(f"ð¥ Loop crashed: {e}")
            await asyncio.sleep(INTERVAL)

# --------------- BOT COMMANDS -------------

@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    await msg.reply("ð¤ Bot is online!", parse_mode=ParseMode.HTML)

@dp.message(Command("forcenow"))
async def cmd_forcenow(msg: types.Message):
    await msg.reply("ð Forcing forwardâ¦", parse_mode=ParseMode.HTML)
    global last_message
    if last_message is None:
        msgs = await tel_client.get_messages('me', limit=1)
        if msgs:
            last_message = msgs[0]
    await forward_messages()

@dp.message(Command("addgroup"))
async def cmd_addgroup(msg: types.Message):
    global links
    parts = msg.text.split(maxsplit=1)
    if len(parts) != 2:
        return await msg.reply("â Usage: /addgroup <t.me link>")
    link = parts[1].strip()
    if link not in links:
        links.append(link)
        await msg.reply(f"â Added: {link}")
    else:
        await msg.reply("â ï¸ Already in list.")

@dp.message(Command("removegroup"))
async def cmd_removegroup(msg: types.Message):
    global links
    parts = msg.text.split(maxsplit=1)
    if len(parts) != 2:
        return await msg.reply("â Usage: /removegroup <t.me link>")
    link = parts[1].strip()
    if link in links:
        links.remove(link)
        await msg.reply(f"ðï¸ Removed: {link}")
    else:
        await msg.reply("â ï¸ Not found in list.")

@dp.message(Command("showgroups"))
async def cmd_showgroups(msg: types.Message):
    if links:
        await msg.reply("ð Groups/topics:\n<code>" + "\n".join(links) + "</code>", parse_mode=ParseMode.HTML)
    else:
        await msg.reply("ð­ No groups/topics available.")

@dp.message(Command("reset"))
async def cmd_reset(msg: types.Message):
    """
    /reset <email_or_username> â uses Instagramâs API to send a reset link.
    Reply format improved: shows timestamp, user, and simple success/failure.
    """
    parts = msg.text.split(maxsplit=1)
    if len(parts) != 2:
        return await msg.reply("â Usage: /reset <email or username>")

    user_input = parts[1].strip()
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    def send_reset(target: str):
        if target.startswith("@"):
            return False, "Enter without '@'"

        data = {
            "_csrftoken": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "guid": str(uuid.uuid4()),
            "device_id": str(uuid.uuid4())
        }

        if "@" in target:
            data["user_email"] = target
        else:
            data["username"] = target

        headers = {
            "user-agent": (
                "Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; "
                f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/"
                f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; "
                f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
            )
        }

        try:
            r = requests.post(
                "https://i.instagram.com/api/v1/accounts/send_password_reset/",
                headers=headers,
                data=data
            )
            return ("obfuscated_email" in r.text), r.text
        except Exception as e:
            return False, str(e)

    success, result = send_reset(user_input)
    if success:
        await msg.reply(
            f"â Reset sent!\nð Time: {now}\nð¤ User: @xitaf3\nð¬ Status: success",
            parse_mode=ParseMode.HTML
        )
    else:
        try:
            error_json = json.loads(result)
            error_msg = error_json.get("message", result)
        except Exception:
            error_msg = result[:200]

        await msg.reply(
            f"â Reset failed\nâ  Message: {error_msg}",
            parse_mode=ParseMode.HTML
        )

# --------------- MAIN ---------------------
async def main():
    await asyncio.gather(
        dp.start_polling(bot, skip_updates=True),
        forward_messages()
    )

if __name__ == "__main__":
    asyncio.run(main())