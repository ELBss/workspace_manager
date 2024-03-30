import aiohttp
import json

URL = ''

async def qwe(data):
    
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + 'check_id/', json=json) as response:
            r = await response.json()
