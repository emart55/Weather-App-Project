import csv
from datetime import datetime

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees celcius."
    """
    return f"{temp}{DEGREE_SYBMOL}"


def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.

    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    from datetime import datetime

    # Parse the ISO date into a datetime object
    parsed_date = datetime.fromisoformat(iso_string)

    # Format the datetime object into the desired format
    formatted_date = parsed_date.strftime('%A %d %B %Y')

    return formatted_date


def convert_f_to_c(temp_in_farenheit):
    """Converts an temperature from farenheit to celcius.

    Args:
        temp_in_farenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees celcius, rounded to 1dp.
    """
    int_temp = float(temp_in_farenheit)
    celsius = (int_temp - 32) * 5 / 9
    celsius_rounded = round(celsius, 1)
    
    return celsius_rounded

def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    numeric_numbers = [float(num) for num in weather_data]  # Convert strings to float
    total = sum(numeric_numbers)
    count = len(numeric_numbers)
    average = total/count

    return average


def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    import csv

    with open(csv_file, 'r') as file:
        rows = []  # List to store the rows
        skip_header = True  # Flag to skip the first row
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if skip_header:
                skip_header = False
                continue  # Skip the first row
            if all(not cell.strip() for cell in row):
                continue
            # Convert appropriate numeric values to integers
            converted_row = []
            for cell in row:
                cell = cell.strip()
                try:
                    converted_row.append(int(cell))
                except ValueError:
                    converted_row.append(cell)
            rows.append(converted_row)

        return rows



def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minium value and it's position in the list.
    """
    if not weather_data:
        return () 

    data = data = [float(item) for item in weather_data]

    min_value = min(data)
    min_index = data.index(min_value)

    # Check if there is a second occurrence
    if data.count(min_value) > 1:
        # Find the index of the second occurrence
        min_index = data.index(min_value, min_index + 1)

    return min_value, min_index


def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list.
    """
    if not weather_data:
        return () 

    data = data = [float(item) for item in weather_data]

    max_value = max(data)
    max_index = data.index(max_value)

    # Check if there is a second occurrence
    if data.count(max_value) > 1:
        # Find the index of the second occurrence
        max_index = data.index(max_value, max_index + 1)
            
    return max_value, max_index


def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    #Variables
    min_temp = float('inf')
    min_temp_date = ""
    max_temp = float('-inf')
    max_temp_date = ""
    total_min_temp = 0
    total_max_temp = 0

    #This will find min/max temperatures and calculate totals
    for day in weather_data:
        date_str = day[0]
        datetime_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        day_of_week = datetime_object.strftime("%A %d %B %Y")

        temp_min = convert_f_to_c2(day[1])
        temp_max = convert_f_to_c2(day[2])

    # Update min temperature and date if lower temperature is found
        if temp_min < min_temp:
            min_temp = temp_min
            min_temp_date = day_of_week

    #Update max temperature and date if higher temperature is found
        if temp_max > max_temp:
            max_temp = temp_max
            max_temp_date = day_of_week

    #Accumulate temperatures for averaging
        total_min_temp += temp_min
        total_max_temp += temp_max

    #Calculating the average temperatures
    avg_min_temp = total_min_temp / len(weather_data)
    avg_max_temp = total_max_temp / len(weather_data)

    #The format of the summary info
    summary = "{} Day Overview\n".format(len(weather_data))
    summary += "  The lowest temperature will be {:.1f}°C, and will occur on {}.\n".format(min_temp, min_temp_date)
    summary += "  The highest temperature will be {:.1f}°C, and will occur on {}.\n".format(max_temp, max_temp_date)
    summary += "  The average low this week is {:.1f}°C.\n".format(avg_min_temp)
    summary += "  The average high this week is {:.1f}°C.\n".format(avg_max_temp)

    return summary


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    summary = ""  

    for day in weather_data:
        date_str = day[0]
        datetime_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        day_of_week = datetime_object.strftime("%A %d %B %Y")

        min_temp = convert_f_to_c2(day[1])
        max_temp = convert_f_to_c2(day[2])

        formatted_date = "---- {} ----".format(day_of_week)
        formatted_min_temp = "  Minimum Temperature: {:.1f}°C".format(min_temp)
        formatted_max_temp = "  Maximum Temperature: {:.1f}°C".format(max_temp)

        formatted_output = "\n".join([formatted_date, formatted_min_temp, formatted_max_temp])
        summary += formatted_output + "\n\n"  

    return summary



def convert_f_to_c2(temperature_f):
    return (temperature_f - 32) * 5 / 9

