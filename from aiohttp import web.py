from aiohttp import web
import vk_api
import asyncio

token='e857793a4ecc55efad8627bd0873474822dbf6c111a31929518dd773678e53f57050dd879014fa3979f33'

vk_session = vk_api.vk_api.VkApiGroup(token=token, api_version='5.200')
vk = vk_session.get_api()

routes = web.RouteTableDef()

@routes.get('/')
async def get_handler(request):
    print('get')

@routes.post('/post')
async def post_handler(request):
    print('post')

@routes.put('/put')
async def put_handler(request):
    print('put')

app = web.Application()
#app.add_routes([web.post('/', handle_post)])
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0", port = "23659")