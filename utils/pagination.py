from typing import List
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def paginate(ch_data: List[dict], max_btn_per_page: int, current_page: int = 1, cb_var: str = None) -> InlineKeyboardMarkup:
    total_channels = len(ch_data)
    total_pages = (total_channels + max_btn_per_page - 1) // max_btn_per_page
    start_index = (current_page - 1) * max_btn_per_page
    end_index = min(start_index + max_btn_per_page, total_channels)
    buttons = [
        [InlineKeyboardButton(channel['name'], callback_data=f"{cb_var}_{channel['channel_id']}")]
        for channel in ch_data[start_index:end_index]
    ]
    
    navigation_buttons = []
    if current_page > 1:
        navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"{cb_var}_back_{current_page - 1}"))
    if current_page < total_pages:
        navigation_buttons.append(InlineKeyboardButton("Next", callback_data=f"{cb_var}_next_{current_page + 1}"))
    
    return InlineKeyboardMarkup(buttons + [navigation_buttons] if navigation_buttons else buttons)
