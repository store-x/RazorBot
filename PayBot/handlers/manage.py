from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from PayBot import bot, ADMINS
from database import add_pchat, remove_pchat, list_pchat, chat_exists
from pyrogram.errors import UserNotParticipant
from utils import is_bot_admin


@bot.on_message(filters.command("add_chat") & filters.user(ADMINS))
async def add_chat(client: Client, message: Message):
    await message.reply("Please send the channel ID:")
    channel_id_message = await client.listen(message.chat.id)
    channel_id = int(channel_id_message.text)
    if not await is_bot_admin(client, channel_id):
        await message.reply("The bot needs to be an admin in the channel. Please make it an admin first.")
        return
    if await chat_exists(channel_id):
        await message.reply("This chat is already present in the database.")
        return
    chat_info = await client.get_chat(channel_id)
    default_name = chat_info.title
    await message.reply(f"The default name for this chat is: '{default_name}'. Do you want to use it? (yes/no)")
    name_response = await client.listen(message.chat.id)
    if name_response.text.lower() == "no":
        await message.reply("Please send the new name for the chat:")
        name_message = await client.listen(message.chat.id)
        name = name_message.text
    else: name = default_name
    await message.reply("Please send the price:")
    price_message = await client.listen(message.chat.id)
    price = int(price_message.text)
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
        return await message.reply("No channels available.")
    markup = await paginate(channels, max_btn_per_page=5, current_page=1, cb_var="list_chats")
    await message.reply("📋 **Choose from below Channel List:**", reply_markup=markup)


@bot.on_callback_query(filters.regex(r"^list_chats"))
async def channel_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    
    if len(data) == 2:
        channel_id = int(data[1])
        channels = await list_pchat()
        channel = next((ch for ch in channels if ch['channel_id'] == channel_id), None)
        if channel:
            text = f"🔹 **Name:** {channel['name']}\n" \
                   f"💬 **ID:** {channel['channel_id']}\n" \
                   f"💰 **Price:** ₹{channel['price']}\n" \
                   f"👥 **Users Purchased:** {len(channel['users_purchased'])}\n"
            await callback_query.message.edit_text(text)
        else:
            await callback_query.answer("Channel not found.")
    elif len(data) == 3:
        current_page = int(data[2])
        channels = await list_pchat()
        markup = await paginate(channels, max_btn_per_page=5, current_page=current_page, cb_var="list_chats")
        await callback_query.message.edit_reply_markup(markup)
