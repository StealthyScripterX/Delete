import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 29478891
API_HASH = "43feb597594883965998bdad7cabbaca"
BOT_TOKEN = "8159969687:AAEnd6PhjcpexovxB-iSU9by286Ur1s5ZTY"

app = Client("auto_delete_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)

DEFAULT_MSG_DELAY = 180
DEFAULT_CMD_DELAY = 120

GROUP_SETTINGS = {}


def get_settings(chat_id):
    if chat_id not in GROUP_SETTINGS:
        GROUP_SETTINGS[chat_id] = {
            "msg_delay": DEFAULT_MSG_DELAY,
            "cmd_delay": DEFAULT_CMD_DELAY
        }
    return GROUP_SETTINGS[chat_id]


async def is_admin(client, chat_id, user_id):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "owner")
    except:
        return False


async def safe_delete(chat_id, msg_id):
    try:
        await app.delete_messages(chat_id, msg_id)
    except:
        pass


# 🔥 NORMAL MESSAGES (NOT COMMAND, NOT SERVICE)
@app.on_message(
    filters.group
    & filters.incoming
    & ~filters.regex(r"^/")
    & ~filters.service
)
async def auto_delete_msg(_, message: Message):
    settings = get_settings(message.chat.id)
    await asyncio.sleep(settings["msg_delay"])
    await safe_delete(message.chat.id, message.id)


# ⚡ COMMANDS
@app.on_message(filters.group & filters.incoming & filters.regex(r"^/"))
async def auto_delete_cmd(_, message: Message):
    settings = get_settings(message.chat.id)
    await asyncio.sleep(settings["cmd_delay"])
    await safe_delete(message.chat.id, message.id)


# 📌 PIN SERVICE MESSAGE → IGNORE
@app.on_message(filters.group & filters.service & filters.pinned_message)
async def pinned_event(_, message: Message):
    return


# 🛠 ADMIN: SET MESSAGE DELAY
@app.on_message(filters.group & filters.command("setmsgdelay"))
async def set_msg_delay(client, message: Message):

    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply_text("❌ Admin only command")
        await asyncio.sleep(5)
        await safe_delete(warn.chat.id, warn.id)
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        reply = await message.reply_text("Usage: /setmsgdelay <seconds>")
        await asyncio.sleep(10)
        await safe_delete(reply.chat.id, reply.id)
        return

    delay = int(message.command[1])
    get_settings(message.chat.id)["msg_delay"] = delay

    reply = await message.reply_text(f"✅ Message delete delay set to {delay}s")
    await asyncio.sleep(DEFAULT_CMD_DELAY)
    await safe_delete(reply.chat.id, reply.id)


# 🛠 ADMIN: SET COMMAND DELAY
@app.on_message(filters.group & filters.command("setcmddelay"))
async def set_cmd_delay(client, message: Message):

    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply_text("❌ Admin only command")
        await asyncio.sleep(5)
        await safe_delete(warn.chat.id, warn.id)
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        reply = await message.reply_text("Usage: /setcmddelay <seconds>")
        await asyncio.sleep(10)
        await safe_delete(reply.chat.id, reply.id)
        return

    delay = int(message.command[1])
    get_settings(message.chat.id)["cmd_delay"] = delay

    reply = await message.reply_text(f"✅ Command delete delay set to {delay}s")
    await asyncio.sleep(delay)
    await safe_delete(reply.chat.id, reply.id)


# 📊 ADMIN: STATUS
@app.on_message(filters.group & filters.command("status"))
async def status(client, message: Message):

    if not message.from_user or not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply_text("❌ Admin only command")
        await asyncio.sleep(5)
        await safe_delete(warn.chat.id, warn.id)
        return

    s = get_settings(message.chat.id)
    reply = await message.reply_text(
        f"📊 Auto Delete Status\n\n"
        f"🗑 Messages: {s['msg_delay']}s\n"
        f"⌛ Commands: {s['cmd_delay']}s\n"
        f"📌 Pinned: Safe"
    )
    await asyncio.sleep(s["cmd_delay"])
    await safe_delete(reply.chat.id, reply.id)


if __name__ == "__main__":
    app.run()        return

    delay = int(message.command[1])
    settings = get_settings(message.chat.id)
    settings["msg_delay"] = delay

    reply = await message.reply_text(f"✅ Message delete delay set to {delay}s")
    await asyncio.sleep(settings["cmd_delay"])
    await safe_delete(reply.chat.id, reply.id)


# 🛠 ADMIN: SET COMMAND DELAY
@app.on_message(filters.group & filters.command("setcmddelay"))
async def set_cmd_delay(client, message: Message):

    if not message.from_user:
        warn = await message.reply_text("❌ Cannot identify the sender.")
        await asyncio.sleep(5)
        await safe_delete(warn.chat.id, warn.id)
        return

    if not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply_text("❌ Admin only command")
        await asyncio.sleep(5)
        await safe_delete(warn.chat.id, warn.id)
        return

    if len(message.command) != 2 or not message.command[1].isdigit():
        reply = await message.reply_text("Usage: /setcmddelay <seconds>")
        await asyncio.sleep(10)
        await safe_delete(reply.chat.id, reply.id)
        return

    delay = int(message.command[1])
    settings = get_settings(message.chat.id)
    settings["cmd_delay"] = delay

    reply = await message.reply_text(f"✅ Command delete delay set to {delay}s")
    await asyncio.sleep(settings["cmd_delay"])
    await safe_delete(reply.chat.id, reply.id)


# 📊 ADMIN: STATUS
@app.on_message(filters.group & filters.command("status"))
async def status(client, message: Message):

    if not message.from_user:
        warn = await message.reply_text("❌ Cannot identify the sender.")
        await asyncio.sleep(5)
        await safe_delete(warn.chat.id, warn.id)
        return

    if not await is_admin(client, message.chat.id, message.from_user.id):
        warn = await message.reply_text("❌ Admin only command")
        await asyncio.sleep(5)
        await safe_delete(warn.chat.id, warn.id)
        return

    settings = get_settings(message.chat.id)
    reply = await message.reply_text(
        f"📊 **Auto Delete Status**\n\n"
        f"🗑 Messages: `{settings['msg_delay']}s`\n"
        f"⌛ Commands: `{settings['cmd_delay']}s`\n"
        f"📌 Pinned: Safe"
    )

    await asyncio.sleep(settings["cmd_delay"])
    await safe_delete(reply.chat.id, reply.id)


app.run()
