from datetime import datetime


def determine_time(time_object):
    current_time = datetime.now()
    time_difference = 0

    if (
        time_object.month == current_time.month
        and time_object.year == current_time.year
        and time_object.day == current_time.day
    ):
        time_difference = current_time.hour - time_object.hour
        minutes_difference = current_time.minute - time_object.minute
        if time_difference > 1:
            return f"{time_difference} hours ago"
        if time_difference < 1:
            return f"{minutes_difference} minutes ago"
        else:
            return f"{time_difference} hour ago"
    elif (
        time_object.year == current_time.year
        and time_object.month == current_time.month
        and time_object.day != current_time.day
    ):
        time_difference = current_time.day - time_object.day
        if time_difference > 1:
            return "{} days ago".format(time_difference)
        else:
            return "{} day ago".format(time_difference)
    return "{}/{}/{}".format(time_object.day, time_object.month, time_object.year)
