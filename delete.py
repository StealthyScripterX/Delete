import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 
API_HASH = ""
BOT_TOKEN = ""

app = Client(
    "auto_delete_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Timings
MESSAGE_DELETE_DELAY = 180     # 3 minutes
COMMAND_DELETE_DELAY = 120     # 120 seconds


async def safe_delete(chat_id: int, message_id: int):
    try:
        await app.delete_messages(chat_id, message_id)
    except:
        pass


# 🔥 Group messages auto delete (except pinned)
@app.on_message(filters.group & ~filters.command)
async def auto_delete_messages(_, message: Message):
    if message.pinned_message:
        return

    await asyncio.sleep(MESSAGE_DELETE_DELAY)
    await safe_delete(message.chat.id, message.id)


# ⚡ Commands auto clear after 120 sec
@app.on_message(filters.group & filters.command)
async def auto_delete_commands(_, message: Message):
    await asyncio.sleep(COMMAND_DELETE_DELAY)
    await safe_delete(message.chat.id, message.id)


# Optional reply (will also get deleted)
@app.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    reply = await message.reply_text(
        "🤖 Auto Delete Bot Active!\n"
        "• Messages delete after 3 minutes\n"
        "• Commands delete after 120 seconds\n"
        "• Pinned messages are safe"
    )
    await asyncio.sleep(COMMAND_DELETE_DELAY)
    await safe_delete(reply.chat.id, reply.id)


app.run()
