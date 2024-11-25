from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ChatMemberStatus

from .pagination import paginate 
from PayBot import BOT_ID

async def is_bot_admin(client: Client, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, BOT_ID)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(e)
        return False
