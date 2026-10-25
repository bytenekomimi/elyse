import os, aiohttp, logging
from pathlib import Path
from dotenv import load_dotenv, set_key

load_dotenv()

logger = logging.getLogger(__name__)

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
TwitchID = os.getenv("TBOTID")
TwitchSecret = os.getenv("TBOTSECRET")
TwitchAccessToken = os.getenv("TACCESS")
TwitchLifetime = os.getenv("TLIFETIME")

Token_Url = "https://id.twitch.tv/oauth2/token"
Validate_Url = "https://id.twitch.tv/oauth2/validate"

async def twitchAuthGet():
    payload = {
        "client_id": TwitchID,
        "client_secret": TwitchSecret,
        "grant_type": "client_credentials",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(Token_Url, data=payload) as resp:
            if resp.status != 200:
                error = await resp.text()
                logging.error(error)
                return None
            data = await resp.json()
            return data["access_token"]

async def twitchAuthValidate():
    headers = {
        "Authorization": f"OAuth {TwitchAccessToken}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(Validate_Url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                set_key(key_to_set="TLIFETIME", value_to_set=str(data['expires_in']), dotenv_path=str(ENV_FILE), quote_mode="never")
                logging.info(f"Twitch token valid and expires in {data['expires_in']} seconds")
