import urllib.request
import urllib.parse
from utils import codestats
from utils import current_time


API_VERSION = '5.130'
R_ONE = '"response":1'
R_FIVE = '"error_code":5'
R_EIGHT = '"error_code":8'
R_TWENTY_NINE = '"error_code":29'


def update_status(url, token):
    """Update status on VK using API.

    This function handles almost all functions (Need to simplify it):
    - Get current time
    - Get CodeStats level
    - Parse status text for safe use in URL
    - Get response data and it's status
    - Send console log data

    Args:
        url (str): CodeStats API URL
        token (str): Access token for VK account

    Returns:
        int: Extracted status from response data
    """
    curr_time = current_time.get_current_time()
    status_text = codestats.get_codestats_level(url, curr_time[1])
    parsed_text = urllib.parse.quote(status_text, safe=b'')
    vk_url = 'https://api.vk.com/method/status.set?' \
             f'text={parsed_text}&v={API_VERSION}&access_token={token}'
    response = urllib.request.urlopen(vk_url)
    response_status = check_response_status(
        str(response.read()),
        curr_time[0]
    )
    return response_status


def check_response_status(curr_response, full_time):
    """Check response status and return code of it.
    
    This function also handles printing console log info

    Args:
        curr_response (str): Response from VK API URL
        full_time (str): Full format fime for console log

    Returns:
        int: Status from response data
    """
    if R_ONE in curr_response:
        print(f'[{full_time}] Status has been set successfully! '
              f'Waiting 1 hour to update!')
        return 1
    if R_FIVE in curr_response:
        print('[Error] Access token has been expired or it is wrong. '
              'Please change it and try again!')
        return 5
    if R_EIGHT in curr_response:
        print('[Error] Got deprecated API version or no API version. '
              'Please add/change API version and try again!')
        return 8
    if R_TWENTY_NINE in curr_response:
        print("[Error] Rate limit!")
        print('We are sorry, we can\'t do nothing about this. '
              'All you need is patience. '
              'Please wait before initilizing script again!')
        return 29
    print('[Error] Unknown error! '
          'Here are response string:')
    print(curr_response)
    print('We hope this can help you out to fix this problem!')
    return 0
