from PayBot import db

channels = db["channels"]

async def add_pchat(name: str, channel_id: int, price: int):
    await channels.update_one(
        {"channel_id": channel_id},
        {"$set": {"name": name, "price": price}, "$setOnInsert": {"users_purchased": []}},
        upsert=True,
    )

async def remove_pchat(channel_id: int):
    await channels.delete_one({"channel_id": channel_id})

async def chat_exists(channel_id: int):
    return await channels.find_one({"channel_id": channel_id})
    
async def list_pchat():
    return await channels.find({}).to_list(length=None)

async def edit_pchat_field(channel_id: int, field: str, new_value):
    await channels.update_one(
        {"channel_id": channel_id},
        {"$set": {field: new_value}})

