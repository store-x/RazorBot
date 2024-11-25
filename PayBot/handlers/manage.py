
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from PayBot import bot, ADMINS
from database import add_pchat, remove_pchat, list_pchat

@bot.on_message(filters.command("add_chat") & filters.user(ADMINS))
async def add_chat(client: Client, message: Message):
    if len(message.command) < 4:
        await message.reply("Usage: /add_chat <name> <channel_id> <price>")
        return
    name, channel_id, price = message.command[1], int(message.command[2]), int(message.command[3])
    await add_pchat(name, channel_id, price)
    await message.reply(f"✅ Added channel: {name} (ID: {channel_id}) for ₹{price}")

@bot.on_message(filters.command("remove_chat") & filters.user(ADMINS))
async def remove_chat(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /remove_chat <channel_id>")
        return
    channel_id = int(message.command[1])
    await remove_pchat(channel_id)
    await message.reply(f"✅ Removed channel with ID: {channel_id}")

@bot.on_message(filters.command("list_chats") & filters.user(ADMINS))
async def list_chats(client: Client, message: Message):
    channels = await list_pchat()
    if not channels:
        await message.reply("No channels available.")
        return
    text = "📋 **Channel List:**\n"
    for ch in channels:
        text += f"\n🔹 **Name:** {ch['name']}\n" \
                f"💬 **ID:** {ch['channel_id']}\n" \
                f"💰 **Price:** ₹{ch['price']}\n" \
                f"👥 **Users Purchased:** {len(ch['users_purchased'])}\n"
    await message.reply(text)
