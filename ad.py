import csv
from datetime import datetime, timedelta

# Function to read data from a CSV file and return it as a list of dictionaries
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to find employees who have worked for a specified number of consecutive days
def find_consecutive_days(data, threshold_days=7):
    if not data:
        print("Empty data")
        return

    # Sort data by date
    data.sort(key=lambda x: parse_datetime(x['Time']) if x['Time'] else datetime.min)

    consecutive_days = 0
    max_consecutive_days = 0
    previous_date = None

    # Initialize the employee_records dictionary
    employee_records = {}

    for entry in data:
        # Skip entries with missing 'Time' information
        if not entry['Time']:
            continue

        date = parse_datetime(entry['Time'])

        if previous_date is not None and date == previous_date + timedelta(days=1):
            consecutive_days += 1
        else:
            consecutive_days = 1
        max_consecutive_days = max(max_consecutive_days, consecutive_days)
        previous_date = date

        employee_name = entry['Employee Name']

        # Check if the employee has records in the dictionary and date is not None
        if employee_name not in employee_records:
            employee_records[employee_name] = {'start_date': date, 'consecutive_days': 1}
        elif date:
            # Check if the current date is consecutive to the previous date
            if date - employee_records[employee_name]['start_date'] == timedelta(days=1):
                employee_records[employee_name]['consecutive_days'] += 1
            else:
                # Reset the consecutive days count if the current date is not consecutive
                employee_records[employee_name]['start_date'] = date
                employee_records[employee_name]['consecutive_days'] = 1

            # Print the employee's name if they have worked for the specified consecutive days
            if employee_records[employee_name]['consecutive_days'] == threshold_days:
                print(f"{employee_name} has worked for {threshold_days} consecutive days.")

# Function to find employees with short shifts between specified minimum and maximum hours
def find_short_shifts(data, min_hours=1, max_hours=10):
    for entry in data:
        employee_name = entry['Employee Name']
        time_in = parse_datetime(entry['Time'])
        time_out = parse_datetime(entry['Time Out']) if entry['Time Out'] else None

        # Skip entries with missing time information
        if not time_in or not time_out:
            continue

        shift_hours = (time_out - time_in).total_seconds() / 3600

        # Print the employee's name if they have a short shift
        if min_hours < shift_hours < max_hours:
            print(f"{employee_name} has a short shift with {shift_hours:.2f} hours between shifts.")

# Function to find employees who have worked for more than a specified number of hours in a single shift
def find_long_shifts(data, threshold_hours=14):
    for entry in data:
        employee_name = entry['Employee Name']
        shift_hours = float(entry['Timecard Hours'])

        # Print the employee's name if they have worked for more than the specified hours in a single shift
        if shift_hours > threshold_hours:
            print(f"{employee_name} has worked for more than {threshold_hours} hours in a single shift.")

# Function to parse date-time strings with multiple formats
def parse_datetime(datetime_str):
    formats = ["%m/%d/%Y %I:%M %p", "%m-%d-%Y %I:%M:%S", "%m-%d-%Y %I:%M"]
    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Cannot parse date-time: {datetime_str}")

# Main function to execute the program
def main():
    file_path = 'Assignment_Timecard.xlsx - Sheet1.csv'  # Replace with the actual path to your CSV file
    data = read_csv(file_path)

    # Call the functions to perform analyses and print results
    find_consecutive_days(data)
    find_short_shifts(data)
    find_long_shifts(data)

# Entry point of the program
if __name__ == "__main__":
    main()
