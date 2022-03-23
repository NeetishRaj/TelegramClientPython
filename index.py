import json
import re
import telethon
from telethon import TelegramClient, events
with open('config.json', encoding='UTF-8') as json_file:
    config = json.load(json_file)
channel_list = config['channel_list']
api_id = config["api_id"]
api_hash = config["api_hash"]
client = TelegramClient('main', api_id, api_hash)
def push_info_to_db(title, address):
    pass
# , chats=channel_list
@client.on(events.NewMessage(chats=channel_list))
async def add_announcement(event: telethon.events.newmessage.NewMessage.Event):
    message = event.raw_text
    a = re.findall(r'(0x[A-Za-z0-9]{40})', message)
    if len(a) > 0:
        push_info_to_db(event.chat.title, a[0])
client.start()
client.run_until_disconnected()