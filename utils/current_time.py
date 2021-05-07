import datetime


def get_current_time():
    """Get current time and return a list of two variants.

    This functions returns two variables: One with full formatting
    and one with short

    Returns:
        list: Variants of full time and short time
    """
    curr_time = datetime.datetime.now()
    full_time = curr_time.strftime("%d.%m.%Y / %H:%M:%S")
    short_time = curr_time.strftime("%H:%M")
    return [full_time, short_time]
