# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import logging
from pyrogram import filters, errors
from WebStreamer.server.stream_routes import db
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils import get_name
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@StreamBot.on_message((filters.video | filters.document) & filters.chat(Var.BIN_CHANNEL) & (filters.InvertFilter(filters.me)))
async def on_new_video(_, m: Message):
    logger.info(f"Generated link: '{Var.URL}videos/{m.id}' for {m.from_user.first_name}")

    db.add_video(m.id, get_name(m), f"{Var.URL}videos/{m.id}")

@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(_, m: Message):
    if Var.ALLOWED_USERS and not ((str(m.from_user.id) in Var.ALLOWED_USERS) or (m.from_user.username in Var.ALLOWED_USERS)):
        return await m.reply("You are not <b>allowed to use</b> this <a href='https://github.com/EverythingSuckz/TG-FileStreamBot'>bot</a>.", quote=True)
    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    stream_link = f"{Var.URL}videos/{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    db.add_video(log_msg.id, get_name(m), stream_link)
    try:
        await m.reply_text(
            text="<code>{}</code>\n".format(
                stream_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open", url=stream_link)]]
            ),
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="<code>{}</code>\n\n)".format(
                stream_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )
