from datetime import datetime

def fetchFormattedDate(date):
    def get_day_suffix(day):
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        return suffix

    day = date.day
    month_name = date.strftime('%B')
    year = date.year

    formatted_date = f"{day}{get_day_suffix(day)} {month_name} {year}"

    return formatted_date
