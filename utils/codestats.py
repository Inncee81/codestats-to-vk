import math
import requests
import random


CODESTATS_LEVEL_FACTOR = 0.025
LANGUAGES = ["Set your own languages to get level"]


def get_codestats_level(url, update_time):
    """Get current account data and extract XP.

    This function also returns level of randomly
    chosen language from list above

    Args:
        url (str): API URL to get data
        update_time (str): Time of current request

    Returns:
        str: Updated status text
    """
    codestats_request = requests.get(url = url)
    acc_data = codestats_request.json()
    random_language = random.choice(LANGUAGES)
    level_xp = acc_data["languages"][random_language]["xps"]
    current_level = int(math.floor(CODESTATS_LEVEL_FACTOR * math.sqrt(level_xp)))
    status_text = f'Current {random_language} level: {current_level} ' \
                  f'| Updated at {update_time}'
    return status_text
