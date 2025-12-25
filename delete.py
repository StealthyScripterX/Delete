import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = "29478891"
API_HASH = "43feb597594883965998bdad7cabbaca"
BOT_TOKEN = "8159969687:AAEnd6PhjcpexovxB-iSU9by286Ur1s5ZTY"

app = Client(
    "auto_delete_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

MESSAGE_DELETE_DELAY = 180   # 3 min
COMMAND_DELETE_DELAY = 120   # 120 sec


async def safe_delete(chat_id, msg_id):
    try:
        await app.delete_messages(chat_id, msg_id)
    except:
        pass


# 🔥 Normal group messages (not commands)
@app.on_message(filters.group & ~filters.command([]))
async def auto_delete_messages(_, message: Message):
    if message.pinned_message:
        return

    await asyncio.sleep(MESSAGE_DELETE_DELAY)
    await safe_delete(message.chat.id, message.id)


# ⚡ Commands delete
@app.on_message(filters.group & filters.command([]))
async def auto_delete_commands(_, message: Message):
    await asyncio.sleep(COMMAND_DELETE_DELAY)
    await safe_delete(message.chat.id, message.id)


@app.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    reply = await message.reply_text(
        "🤖 Auto Delete Bot Active\n"
        "• Messages delete after 3 min\n"
        "• Commands delete after 120 sec\n"
        "• Pinned messages safe"
    )
    await asyncio.sleep(COMMAND_DELETE_DELAY)
    await safe_delete(reply.chat.id, reply.id)


app.run()
