from pyrogram import Client
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

# TIP: Delete the message from callback before calling this
# TIP: Pass any `int` value(like 1) or any `str` value (like 'a') in a_type(answer_type) according to need
# TIP: You can pass allowed valuse set like `{'yes', 'no'}`
async def listen(client: Client, user_id: int, a_type: int | str, d_msg: str, e_msg: str, allowed_values: set = None):
    await client.send_message(user_id, d_msg)
    while True:
        msg = await client.listen(chat_id=user_id)
        if msg.text is None:
            await client.send_message(user_id, e_msg)
            continue
        if allowed_values is not None and msg.text not in allowed_values:
            await client.send_message(user_id, e_msg)
            continue
        if isinstance(a_type, int):
            if not msg.text.isdigit():
                await client.send_message(user_id, e_msg)
                continue
            return int(msg.text)
        elif isinstance(a_type, str):
            return msg.text