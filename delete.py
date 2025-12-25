import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 29478891
API_HASH = "43feb597594883965998bdad7cabbaca"
BOT_TOKEN = "8159969687:AAEnd6PhjcpexovxB-iSU9by286Ur1s5ZTY"

MSG_DELAY = 180
CMD_DELAY = 120

app = Client(
    "auto_delete_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1
)

def is_real_user(m: Message):
    return bool(m.from_user) and not m.sender_chat

async def safe_delete(m: Message, delay: int):
    try:
        await asyncio.sleep(delay)
        await m.delete()
    except:
        pass

@app.on_message(filters.group & filters.incoming)
async def handler(_, m: Message):

    # ignore service messages
    if m.service:
        return

    # ignore anonymous/channel
    if not is_real_user(m):
        return

    # ignore pinned
    if m.pinned_message:
        return

    # command
    if m.text and m.text.startswith("/"):
        asyncio.create_task(safe_delete(m, CMD_DELAY))
    else:
        asyncio.create_task(safe_delete(m, MSG_DELAY))

print("🤖 Bot running clean…")
app.run()
