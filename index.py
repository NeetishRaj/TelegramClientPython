import json
import re
import time
import requests
import telethon
import boto3
from boto3.dynamodb.conditions import Attr
from telethon import TelegramClient, events
with open('config.json', encoding='UTF-8') as json_file:
    config = json.load(json_file)
channel_list = config['channel_list']
api_id = config["api_id"]
api_hash = config["api_hash"]
client = TelegramClient('main', api_id, api_hash)
aws_access_key_id = config['aws_access_key_id']
aws_secret_access_key = config['aws_secret_access_key']
region_name = config['region_name']
table_name = config['table_name']
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)
table = dynamodb.Table(table_name)
def push_info_to_db(id_time, channel_id, title, pair_name, address, chain, tbl):
    tbl.put_item(
        Item={
            'id': str(id_time),
            'channel_id': channel_id,
            'channel_name': title,
            'pair_name': pair_name,
            'contract': address,
            'chain': chain
        }
    )
def check_and_delete(channel_id, chain):
    try:
        response = table.scan(FilterExpression=Attr('channel_id').eq(channel_id)&Attr('chain').eq(chain))
    except:
        return
    result = sorted(response['Items'], key=lambda x: x['id'])
    for i in range(len(result) - 100):
        try:
            table.delete_item(Key={'id': result[i]['id']})
        except:
            pass
        time.sleep(2)
def get_pair_name(address):
    a = requests.get("https://aeyp0uqbrf.execute-api.us-east-1.amazonaws.com/token-pair-name-from-address?id={}".format(address))
    return a.text
@client.on(events.NewMessage(chats=channel_list))
async def listen_for_contract(event: telethon.events.newmessage.NewMessage.Event):
    global table
    message = event.raw_text
    contract_links = re.findall(r'(https://www\.dextools\.io.*0x[A-Za-z0-9]{40})', message)
    # print(contract_links)
    id_time = int(time.time())
    for link in contract_links:
        chain = link.split('/')[-3]
        contract_address = link.split('/')[-1]
        push_info_to_db(id_time=id_time,
                        channel_id=str(event.chat_id)[1:],
                        title=event.chat.title,
                        pair_name=get_pair_name(contract_address),
                        address=contract_address,
                        chain=chain,
                        tbl=table)
        check_and_delete(channel_id=str(event.chat_id)[1:], chain=chain)
    contract_links = re.findall(r'(https://dexscreener\.com.*0x[A-Za-z0-9]{40})', message)
    # print(contract_links)
    id_time = int(time.time())
    for link in contract_links:
        chain = link.split('/')[-2]
        contract_address = link.split('/')[-1]
        push_info_to_db(id_time=id_time,
                        channel_id=str(event.chat_id)[1:],
                        title=event.chat.title,
                        pair_name=get_pair_name(contract_address),
                        address=contract_address,
                        chain=chain,
                        tbl=table)
        check_and_delete(channel_id=str(event.chat_id)[1:], chain=chain)
client.start()
client.run_until_disconnected()