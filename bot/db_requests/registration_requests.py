import aiohttp

URL = "http://localhost:8888/"


async def check_id(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + 'check_id/', json={'user_id': user_id}) as response:
            r = await response.json()
            if not r['result']:
                return False


async def send_mail(nickname):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + 'check_mail/', json={'nickname': nickname}) as response:
            r = await response.json()


async def send_code(nickname, code):
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + 'check_code/', json={'nickname': nickname, 'code': code}) as response:
            r = await response.json()
            return r['result']
