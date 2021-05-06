import math
import asyncio
import datetime
import requests
import urllib.request
import urllib.parse

# CodeStats URL for selected profile information
# You can enter your profile name here
CODESTATS_URL = "https://codestats.net/api/users/..."
CODESTATS_LEVEL_FACTOR = 0.025
CODESTATS_REQUEST = requests.get(url = CODESTATS_URL)
ACCOUNT_DATA = CODESTATS_REQUEST.json()
# If you want to get another data, you can change it here
# For more info about data in JSON, go here - https://codestats.net/api-docs#profile
# This example uses Python XP to display
PYTHON_XP = ACCOUNT_DATA["languages"]["Python"]["xps"]
# VK access token to change status text
# You can get one here - https://oauth.vk.com/authorize?client_id=6121396&scope=66560&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1
# This link gives you token only for status access at any time
VK_ACCESS_TOKEN = "..."
# Responses codes of VK API
R_ONE = '"response":1'  # Status has been set
R_FIVE = '"error_code":5'  # No access token provided
R_EIGHT = '"error_code":8'  # API version has been deprecated or not present in link
R_TWENTY_NINE = '"error_code":29'  # Rate limit reached

# This function returns full_time for console logging and short_time for displaying in final status
# Can be removed or changed for other needs
def get_current_time():
    full_time = datetime.datetime.now().strftime("%d.%m.%Y / %H:%M:%S")
    short_time = datetime.datetime.now().strftime("%H:%M")
    return [full_time, short_time]

# This function convert current XP of language to level integer using CodeStats formula
# More about it here - https://codestats.net/api-docs#terms
def get_codestats_level(current_xp, update_time):
    # This text is an example of what you can set as a status
    return f"Current Python level: {int(math.floor(CODESTATS_LEVEL_FACTOR * math.sqrt(current_xp)))} | Updated at {update_time}"

# This function updates status on VK and returns response data
def update_status(curr_time):
    status_text = get_codestats_level(PYTHON_XP, curr_time)
    vk_url = f"https://api.vk.com/method/status.set?text={urllib.parse.quote(status_text, safe=b'')}&v=5.130&access_token={VK_ACCESS_TOKEN}"
    response = urllib.request.urlopen(vk_url)
    return str(response.read())

# This function checks response data and return code of response
def check_request_status(curr_response):
    if R_ONE in curr_response:
        return 1
    elif R_FIVE in curr_response:
        return 5
    elif R_EIGHT in curr_response:
        return 8
    elif R_TWENTY_NINE in curr_response:
        return 29
    else:
        return 0

# This function serves as main asynchronius loop
# Every one hour, it updates status on VK
async def main_loop():
    while True:
        # Get list of current time (Short and Full variants)
        current_time = get_current_time()
        # Update status text and get request data
        response_data = update_status(current_time[1])
        # Check response status and return response code
        response_status = check_request_status(response_data)
        if response_status == 1:
            # Printing log info
            print(f"[{current_time[0]}] Status has been set successfully! Waiting 1 hour to update!")
            # Wait for 1 hour
            await asyncio.sleep(3600)
        if response_status == 5:
            # Printing error log and exiting from script
            print('Seems like your access token has been expired or it is wrong. Please correct it and try again!')
            raise SystemExit
        if response_status == 8:
            # Printing error log and exiting from script
            print('Seems like you entered deprecated API version or even forgot to add it. Please add API version and try again!')
            raise SystemExit
        if response_status == 29:
            # Printing error log and exiting from script
            print("Oops, you have faced with Rate limit. We are sorry, we can't do nothing about this. All you need is patience. Please wait some time (maybe even 24 hours) before initilizing script again!")
            raise SystemExit
        if not response_status:
            # Printing error log, response status and exiting from script
            print('There is an unknown error! Here are response string to get you in touch with trouble:')
            print(response_status)
            print('We hope this can help you out to fix this problem!')
            raise SystemExit

# Execute asynchronius loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop())
