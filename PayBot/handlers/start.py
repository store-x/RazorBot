from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from PayBot import bot, BOT_NAME
from database import list_pchat
from utils import paginate

@bot.on_message(filters.command("start") & ~filters.private)
async def start_in_group(client: Client, message: Message):
    await message.reply(
        "👋 **Hello!**\n\nThis bot works only in private chats. Please message me directly to get started.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🤖 Message Me", url=f"t.me/{bot.me.username}")]])
    )

@bot.on_message(filters.command("start") & filters.private)
async def start_in_private(client: Client, message: Message):
    await message.reply(
        f"👋 **Welcome to {BOT_NAME}!**\n"
        "Explore and unlock exclusive Telegram channels effortlessly. 🚀\n\n"
        "Use the buttons below to navigate through the bot's features.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔍 Browse Channels", callback_data="browse_channels")],
                [InlineKeyboardButton("ℹ️ Help", callback_data="help"), InlineKeyboardButton("🛒 My Purchases", callback_data="my_purchases")],
            ]
        )
    )

@bot.on_callback_query(filters.regex(r"^browse_channels"))
async def browse_channels_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    if len(data) == 2:
        channels = await list_pchat()
        if not channels:
            return await callback_query.answer("No channels available.", show_alert=True)
        markup = await paginate(channels, max_btn_per_page=5, current_page=1, cb_var="browse_channels")
        await callback_query.message.edit_text("📋 **Explore Available Channels:**", reply_markup=markup)
    elif len(data) == 4:
        current_page = int(data[3])
        channels = await list_pchat()
        markup = await paginate(channels, max_btn_per_page=5, current_page=current_page, cb_var="browse_channels")
        await callback_query.message.edit_reply_markup(markup)
