import os

import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

TSECRET = os.getenv("TBOTSECRET")
TID = os.getenv("TBOTID")
TACCESS = os.getenv("TACCESS")

async def main():
    #payload = {
    #    "client_id": TID,
    #    "client_secret": TSECRET,
    #    "grant_type": "client_credentials"
    #}
    #async with aiohttp.ClientSession() as session:
    #    async with session.post("https://id.twitch.tv/oauth2/token", data=payload) as resp:
    #        print(resp.status)
    #        print(await resp.json())
    params = {"user_login": "protostar"}
    headers = {"Authorization": f"Bearer {TACCESS}",
               "Client-Id": TID
              }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("https://id.twitch.tv/helix/streams", params=params) as resp:
            resp.raise_for_status()
            print(await resp.json())
asyncio.run(main())