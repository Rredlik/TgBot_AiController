import asyncio
import json
import uuid

import aiohttp

from config import Env

token = 'ZTQwMDNjMjAtMTZkMC00MzMxLWI4NzAtYzFjMTlkMmEzYWQ1OjY2MTQyOGNlLTUxZjctNDAxOC05YzEyLTczMjgxNTQxZDY4YQ=='


async def get_auth(auth_token):
    rq_uid = str(uuid.uuid4())
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': f'{rq_uid}',
        'Authorization': f'Bearer {auth_token}'}
    async with aiohttp.ClientSession() as session:
        response = await session.post(url,
                                      data=payload,
                                      headers=headers,
                                      ssl=False)
        return (await response.json())['access_token']


async def send_requests(prompt):
    giga_token = await get_auth(Env.SBER_AUTH_DATA)
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {giga_token}'
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(url,
                                      data=payload,
                                      headers=headers,
                                      ssl=False)
        return await response.json()


# 1713206017559
if __name__ == '__main__':
    print(asyncio.run(send_requests('Что делать если хочется спать')))
