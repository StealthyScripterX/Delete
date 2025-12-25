import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# ============ CONFIG ============

API_ID = 29478891
API_HASH = "43feb597594883965998bdad7cabbaca"
BOT_TOKEN = "8159969687:AAEnd6PhjcpexovxB-iSU9by286Ur1s5ZTY"

DEFAULT_MSG_DELAY = 180   # 3 minutes
DEFAULT_CMD_DELAY = 120   # 120 seconds

# ===============================

app = Client(
    "auto_delete_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1
)

GROUP_SETTINGS = {}

# ============ HELPERS ============

def get_settings(chat_id):
    if chat_id not in GROUP_SETTINGS:
        GROUP_SETTINGS[chat_id] = {
            "msg_delay": DEFAULT_MSG_DELAY,
            "cmd_delay": DEFAULT_CMD_DELAY
        }
    return GROUP_SETTINGS[chat_id]


def is_real_user(message: Message) -> bool:
    if message.sender_chat:
        return False
    if not message.from_user:
        return False
    return True


async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "owner")
    except:
        return False


async def safe_delete(message: Message, delay: int):
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except:
        pass


# ============ AUTO DELETE NORMAL MESSAGES ============

@app.on_message(
    filters.group
    & filters.incoming
    & ~filters.regex(r"^/")
    & ~filters.service_messages
)
async def auto_delete_message(_, message: Message):

    if not is_real_user(message):
        return

    if message.pinned_message:
        return

    settings = get_settings(message.chat.id)
    asyncio.create_task(safe_delete(message, settings["msg_delay"]))


# ============ AUTO DELETE COMMANDS ============

@app.on_message(filters.group & filters.incoming & filters.regex(r"^/"))
async def auto_delete_command(_, message: Message):

    if not is_real_user(message):
        return

    settings = get_settings(message.chat.id)
    asyncio.create_task(safe_delete(message, settings["cmd_delay"]))


# ============ ADMIN COMMANDS ============

@app.on_message(filters.group & filters.command("setmsgdelay"))
async def set_msg_delay(client, message: Message):

    if not is_real_user(message) or not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply("❌ Admin only command")
        asyncio.create_task(safe_delete(warn, 5))
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        reply = await message.reply("Usage: /setmsgdelay <seconds>")
        asyncio.create_task(safe_delete(reply, 10))
        return

    delay = int(message.command[1])
    get_settings(message.chat.id)["msg_delay"] = delay

    reply = await message.reply(f"✅ Message delete delay set to {delay}s")
    asyncio.create_task(safe_delete(reply, DEFAULT_CMD_DELAY))


@app.on_message(filters.group & filters.command("setcmddelay"))
async def set_cmd_delay(client, message: Message):

    if not is_real_user(message) or not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply("❌ Admin only command")
        asyncio.create_task(safe_delete(warn, 5))
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        reply = await message.reply("Usage: /setcmddelay <seconds>")
        asyncio.create_task(safe_delete(reply, 10))
        return

    delay = int(message.command[1])
    get_settings(message.chat.id)["cmd_delay"] = delay

    reply = await message.reply(f"✅ Command delete delay set to {delay}s")
    asyncio.create_task(safe_delete(reply, delay))


@app.on_message(filters.group & filters.command("status"))
async def status(client, message: Message):

    if not is_real_user(message) or not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply("❌ Admin only command")
        asyncio.create_task(safe_delete(warn, 5))
        return

    s = get_settings(message.chat.id)
    reply = await message.reply(
        f"📊 Auto Delete Status\n\n"
        f"🗑 Messages: {s['msg_delay']}s\n"
        f"⌛ Commands: {s['cmd_delay']}s\n"
        f"📌 Pinned: Safe"
    )
    asyncio.create_task(safe_delete(reply, s["cmd_delay"]))


# ============ START BOT ============

if __name__ == "__main__":
    print("🤖 Auto Delete Bot Running...")
    app.run()
