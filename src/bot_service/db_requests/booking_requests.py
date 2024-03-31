import aiohttp
import logging

URL = "http://db_service:8080/"

async def book(state_data):
    logging.basicConfig(level=logging.INFO)
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + 'reservations', json={
            'user_id': state_data['user_id'],
            'room_id': '20.0',
            'begin': state_data['begin'],
            'end': state_data['end']
        }) as response:
            logging.info(str(response))
            
            if response == 201:
                return True
            return False
            

    return True
