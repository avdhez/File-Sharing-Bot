import base64

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, SAFELINK_WEBSITE
from helper_func import encode, get_message_id


def make_safelink(telegram_link: str) -> str:
    """Wrap a Telegram bot link with the safelink page (replicates JS btoa())."""
    encoded = base64.b64encode(telegram_link.encode("utf-8")).decode("utf-8")
    return f"{SAFELINK_WEBSITE}?url={encoded}"


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="Forward The First Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote=True)
            continue

    while True:
        try:
            second_message = await client.ask(
                text="Forward The Last Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote=True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    tg_link = f"https://t.me/{client.username}?start={base64_string}"
    safe_link = make_safelink(tg_link)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={safe_link}')]])
    await second_message.reply_text(f"<b>Here Is Your Link</b>\n\n{safe_link}", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="Forward Message From The DB Channel (With Quotes)..\n\nOr Send The DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote=True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    tg_link = f"https://t.me/{client.username}?start={base64_string}"
    safe_link = make_safelink(tg_link)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={safe_link}')]])
    await channel_message.reply_text(f"<b>Here Is Your Link</b>\n\n{safe_link}", quote=True, reply_markup=reply_markup)


# Jishu Developer
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
