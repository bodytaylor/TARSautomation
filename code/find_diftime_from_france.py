import pytz
from datetime import datetime

def time_difference_in_hours(city1, city2):
    try:
        city1_timezone = pytz.timezone(city1)
        city2_timezone = pytz.timezone(city2)
    except pytz.UnknownTimeZoneError:
        return "One or both time zones are not recognized."

    # Get the current time in both cities
    city1_time = datetime.now(city1_timezone)
    city2_time = datetime.now(city2_timezone)

    # Calculate the time difference in hours
    time_diff = (city2_time - city1_time).total_seconds() / 3600

    return time_diff

# Example usage:
paris = 'Europe/Paris'
new_york = 'America/New_York'
time_diff = time_difference_in_hours(paris, new_york)
print(f"Time difference between {paris} and {new_york}: {time_diff} hours")
