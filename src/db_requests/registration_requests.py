import aiohttp
import asyncio

URL = "http://localhost:8888/"


async def check_id(user_id):
    return await get_to_auth('check_id/', {'user_id': user_id})
        

async def send_mail(nickname):
    return await get_to_auth('check_mail/', {'nickname': nickname})


async def send_code(nickname, code, user_id):
    return await get_to_auth('check_code/', {'nickname': nickname, 'code': code, 'user_id': user_id})


async def get_to_auth(endpoint: str, data:dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + endpoint, json=data) as response:
            if response.status == 200:
                r = await response.json()
                while True:
                    async with session.get(URL + r['id']) as response:
                        data = await response.json()
                        if data['status'] == 'ready':
                            result = data['result']
                            break
                    await asyncio.sleep(0.5)
    return result

# async def test():
#     if await check_id(666) != 'None':
#         print(await send_mail('rosmertt'))
#         print(await send_code('rosmertt', '1234', 666))

# asyncio.run(test())
