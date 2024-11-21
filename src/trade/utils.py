from datetime import datetime#, timedelta


def days_until(date_str):
    # Convert the given date string to a datetime object
    target_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    # Get the current date
    current_date = datetime.today()
    
    # Calculate the difference in days
    difference_in_days = (target_date - current_date).days
    
    return difference_in_days+1