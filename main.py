import asyncio
from utils import vk


# CodeStats URL for selected profile information
# You can enter your profile name here
CODESTATS_URL = "https://codestats.net/api/users/..."
# VK access token to change status text
# You can get one here - https://oauth.vk.com/authorize?client_id=6121396&scope=66560&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1
# This link gives you token only for status access at any time
VK_ACCESS_TOKEN = "..."


async def main_loop():
    """Execute main loop with 1 hour delay.

    This function executes asynchronius loop with delay.
    It also executes update_status function and check for correct response
    status

    Raises:
        SystemExit: If response status isn't 1
    """
    while True:
        response_status = vk.update_status(CODESTATS_URL, VK_ACCESS_TOKEN)
        if response_status == 1:
            await asyncio.sleep(3600)
        else:
            raise SystemExit


loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop())
