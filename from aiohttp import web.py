from aiohttp import web
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
import requests
import time
#https://discord.com/app/invite-with-guild
token='token'
group_id1 = 
secret_key = 'secret'
server_id = 5
url = 'http://transfer.commanda.keenetic.link/post'
title = 'newTest'

token='token'
vk_session = vk_api.vk_api.VkApiGroup(token=token, api_version='5.200')
vk = vk_session.get_api()

#vk.groups.editCallbackServer(group_id=group_id1, server_id=server_id, url=url, title=title, secret_key=secret_key)

confirmation_code = vk.groups.getCallbackConfirmationCode(access_token=token, group_id=group_id1)['code']

routes = web.RouteTableDef()

def send_message(peer_id,group_id,textFW,conversation_message_id, keyboard_message=None):
    
    fwmsg = {"peer_id":peer_id,"is_reply":1,"conversation_message_ids":conversation_message_id}
    fwmsgJson = json.dumps(fwmsg)
    
    if keyboard_message == None:
        vk.messages.send(peer_id=peer_id, group_id=group_id, message=textFW,random_id=vk_api.utils.get_random_id(), forward=fwmsgJson)
    else: 
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_callback_button(label='Кнопка 1', payload=['button_1'], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_callback_button(label='Discord', payload=['open_discord_link'], color=VkKeyboardColor.PRIMARY)
        vk.messages.send(peer_id=peer_id, group_id=group_id, message=textFW,random_id=vk_api.utils.get_random_id(), forward=fwmsgJson, keyboard=keyboard.get_keyboard())

@routes.post('/post')
async def hello(request):
    
    data = await request.json()
    message_type = data['type']

    if message_type == 'confirmation':
        return web.Response(text=confirmation_code)
    
    elif message_type == 'message_new':
        group_id = data['group_id']#int
        event_id = data['event_id']#int
        date = data['object']['message']['date']
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
        
        word_set = set(['aboba','glad','ранг','клавиатура'])    
        phrase_set = set(text.split())
        #|||||||||||||||||||||||||||||
        if word_set.intersection(phrase_set) == set(['aboba']):
            
            textFW = "abobus"
            send_message(peer_id,group_id,textFW,conversation_message_id)
            
        elif word_set.intersection(phrase_set) == set(['glad']):
            
            textFW = f"valakas"
            send_message(peer_id,group_id,textFW,conversation_message_id)
            
        elif word_set.intersection(phrase_set) == set(['ранг']):
            link = 'https://api.opendota.com/api/players/146636026'
            r = requests.get(link)
            data = r.json()
            textFW = data['rank_tier']
            
        elif word_set.intersection(phrase_set) == set(['клавиатура']):
            textFW = "Клавиатура отправлена"
            send_message(peer_id,group_id,textFW,conversation_message_id,keyboard_message=True)
            
        return web.Response(text='ok')
    
    elif message_type == 'message_event':
        button_group_id = data['group_id']#int
        button_user_id = data['object']['user_id']
        button_peer_id = data['object']['peer_id']#int
        button_event_id = data['object']['event_id']#int
        button_payload = data['object']['payload']
        button_secret = data['secret']
        
        if button_payload[0] == "button_1":
            snack = {"type": "show_snackbar","text": "Тут нихуя нет"}
        elif button_payload[0] == "open_discord_link": 
            snack = {"type": "open_link","link": "https://discord.gg/"}
            
        event_data = json.dumps(snack)
        try:
            vk.messages.sendMessageEventAnswer(event_id = button_event_id,
                                                user_id = button_user_id,
                                                peer_id = button_peer_id,
                                                event_data = event_data)
        except Exception as err:
            print(err)
                            
        #return web.Response(text='ok')
    return web.Response(text='ok')

app = web.Application()

app.add_routes(routes)
web.run_app(app, host="0.0.0.0", port = 23659)
