from async_timeout import timeout
from lcu import lockfile
import aiohttp
import asyncio
from pprint import pp, pprint


async def leave_lobby(timeout_in_seconds: int = 30):
    member_joined = False
    pp("waiting for someone to join...")
    async with aiohttp.ClientSession() as session:
        while member_joined == False:

            url = f'https://127.0.0.1:{lockfile.port}/lol-lobby/v2/lobby'

            headers = {'accept': 'application/json',
                    'Authorization': f'Basic {lockfile.auth}', 'Content-Type': 'application/json'}

            r = await session.get(url, headers=headers, verify_ssl=False)

            file = await r.json()
            if len(file['members']) > 1:
                member_joined = True
                print("Leaving the lobby now...")
                url = f'https://127.0.0.1:{lockfile.port}/lol-lobby/v2/lobby'
                await session.delete(url=url, headers=headers, verify_ssl=False)
                break
            await asyncio.sleep(1)
