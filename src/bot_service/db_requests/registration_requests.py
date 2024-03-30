from time import sleep
import aiohttp
import asyncio
import requests

URL = "http://auth_service:8888/"


async def check_id(user_id):
    tmp = await get_to_auth('check_id/', {'user_id': user_id})
    print()
    print()
    print(tmp)
    print()
    print()
    return tmp
        

async def send_mail(nickname):
    return await get_to_auth('check_mail/', {'nickname': nickname})


async def send_code(nickname, code, user_id):
    return await get_to_auth('check_code/', {'nickname': nickname, 'code': code, 'user_id': user_id})


async def get_to_auth(endpoint: str, data:dict):
    
    response = requests.post(URL + endpoint, json=data)
    if response.status_code != 200:
                raise Exception("AAAAAA")
    r = response.json()
    
    for i in range(10):
        response = requests.get(URL + r['id'])

        if response.status_code == 200:
                data = response.json()
                return data
    
    raise Exception("BBBBB")


    async with aiohttp.ClientSession() as session:
        print("Enter to function", flush=True)
        async with session.post(URL + endpoint, json=data) as response:
            if response.status == 200:
                r = await response.json()
        for i in range(10):
            # while True:
            print( URL + r['id'] )
            async with session.get(URL + r['id']) as response:
                data = await response.json()
                if data['status'] == 'ready':
                    print("Hurray!!!!", flush=True)
                    return data['result']
                    # break
            sleep(0.5)

    # return result

# async def test():
#     if await check_id(666) != 'None':
#         print(await send_mail('rosmertt'))
#         print(await send_code('rosmertt', '1234', 666))

# asyncio.run(test())
