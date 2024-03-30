import aiohttp
import logging

# URL = 'http://10.54.201.35:8080/reservations'
URL = 'https://workspace-manager.onrender.com/reservations'


async def book(state_data):
    logging.basicConfig(level=logging.INFO)
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json={
            'user_id': state_data['user_id'],
            'room_id': '20.0',
            'begin': state_data['begin'],
            'end': state_data['end']
        }) as response:
            r = await response.json()
            logging.info(str(r))
    return True
