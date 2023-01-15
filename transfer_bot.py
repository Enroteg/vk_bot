import vk_api#import govna
import requests
import json
import re
from flask import Flask, request
import time

app = Flask(__name__)

token='e857793a4ecc55efad8627bd0873474822dbf6c111a31929518dd773678e53f57050dd879014fa3979f33'
group_id1 = 194284961
secret_key = '65193637EB7F4FC5335BD31D581FA'
server_id = 5
url = 'http://transfer.commanda.keenetic.link'
title = 'newTest'

vk_session = vk_api.vk_api.VkApiGroup(token=token)
vk = vk_session.get_api()

#важная хуйня!!!!!!!
#vk.groups.editCallbackServer(group_id=group_id, server_id=server_id, url=url, title=title, secret_key=secret_key)

confirmation_code = vk.groups.getCallbackConfirmationCode(access_token=token, group_id=group_id1)['code']

def send_message(peer_id,group_id,textFW,conversation_message_id):
    
    fwmsg = {"peer_id":peer_id,"is_reply":1,"conversation_message_ids":conversation_message_id}
    fwmsgJson = json.dumps(fwmsg)
    vk.messages.send(peer_id=peer_id, group_id=group_id, message=textFW,random_id=vk_api.utils.get_random_id(), forward=fwmsgJson)
    
@app.route('/', methods=['POST'])
def bot():
    data = request.get_json(force=True, silent=True)
    Mtype = data['type']#str
    
    if Mtype == 'confirmation':#confirmation
        return confirmation_code
    
    elif Mtype == 'message_new':
        print('get')
        group_id = data['group_id']#int
        event_id = data['event_id']#int
        from_id = data['object']['message']['from_id']#int
        id = data['object']['message']['id']#int
        attachments = data['object']['message']['attachments']#xyeta
        conversation_message_id = data['object']['message']['conversation_message_id']#int
        fwd_messages = data['object']['message']['fwd_messages']#str + dict
        peer_id = data['object']['message']['peer_id']#int
        text = data['object']['message']['text'].lower()#str
        
        try:#markAsRead
            vk.messages.markAsRead(peer_id=peer_id, start_message_id=id ,mark_conversation_as_read=True)
        except Exception as err:
            print(err)
        
        word_set = set(['aboba','glad','ранг'])    
        phrase_set = set(text.split())
        #|||||||||||||||||||||||||||||
        if word_set.intersection(phrase_set) == set(['aboba']):
            
            textFW = "abobus"
            send_message(peer_id,group_id,textFW,conversation_message_id)
            
        elif word_set.intersection(phrase_set) == set(['glad']):
            
            textFW = "valakas"
            send_message(peer_id,group_id,textFW,conversation_message_id)
            
        elif word_set.intersection(phrase_set) == set(['ранг']):
            
            link = 'https://api.opendota.com/api/players/146636026'
            r = requests.get(link)
            data = r.json()
            textFW = data['rank_tier']
            
            send_message(peer_id,group_id,textFW,conversation_message_id)
            
        return 'ok'
            
    return 'ok'
if __name__ == '__main__':#start
    app.run(host="0.0.0.0", port = "23659", ssl_context="adhoc")