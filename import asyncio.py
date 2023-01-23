import vk_api#import govna
import requests
import json
import re
#from flask import Flask, request
from aiohttp import web
from apscheduler.schedulers.background import BackgroundScheduler
import time

token='e857793a4ecc55efad8627bd0873474822dbf6c111a31929518dd773678e53f57050dd879014fa3979f33'
group_id1 = 194284961
secret_key = '65193637EB7F4FC5335BD31D581FA'
server_id = 5
url = 'http://transfer.commanda.keenetic.link'
title = 'newTest'

vk_session = vk_api.vk_api.VkApiGroup(token=token, api_version='5.200')
vk = vk_session.get_api()


confirmation_code = vk.groups.getCallbackConfirmationCode(access_token=token, group_id=group_id1)['code']

#@app.route('/', methods=['POST'])
routes = web.RouteTableDef()

@routes.post('/post')
async def handle(request):
    #name = request.match_info
    print(request.method)
    return 'ok'


app = web.Application()
#app.add_routes([web.post('/', handle)])
app.router.add_routes(routes)
if __name__ == '__main__':#start
    web.run_app(app, host="0.0.0.0", port = "23659")#, ssl_context="adhoc")
    #app.run(host="0.0.0.0", port = "23659", ssl_context="adhoc")