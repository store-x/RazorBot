from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Import the bot instance
from PayBot import bot, BOT_NAME

@bot.on_message(filters.command("start") & ~filters.private)
async def start_in_group(client: Client, message: Message):
    """
    Handle the /start command in group chats.
    Inform users to use the bot in private chat.
    """
    await message.reply(
        "👋 **Hello!**\n\nThis bot works only in private chats. Please message me directly to get started.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🤖 Message Me", url=f"t.me/{bot.me.username}")]]
        )
    )


@bot.on_message(filters.command("start") & filters.private)
async def start_in_private(client: Client, message: Message):
    """
    Handle the /start command in private chats.
    Show the welcome message and main menu buttons.
    """
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

