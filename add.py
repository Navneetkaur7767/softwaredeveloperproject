import csv
from datetime import datetime, timedelta
from dateutil import parser

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
    data.sort(key=lambda x: parser.parse(x['Time']) if x['Time'] else datetime.min)

    consecutive_days = 0
    max_consecutive_days = 0
    previous_date = None

    # Initialize the employee_records dictionary
    employee_records = {}

    for entry in data:
        # Skip entries with missing 'Time' information
        if not entry['Time']:
            continue

        date = parser.parse(entry['Time'])

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

    if max_consecutive_days < threshold_days:
                print(f"No employee has worked for {threshold_days} consecutive days.")

# Function to find employees with short shifts between specified minimum and maximum hours
def find_short_shifts(data, min_hours=1, max_hours=10):
    for entry in data:
        employee_name = entry['Employee Name']
        time_in = parser.parse(entry['Time']) if entry['Time'] else None
        time_out = parser.parse(entry['Time Out']) if entry['Time Out'] else None

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

        # Use get method to handle the case when 'Timecard Hours' is not present in the entry
        shift_hours = float(entry.get('Timecard Hours', 0))

        # Print the employee's name if they have worked for more than the specified hours in a single shift
        if shift_hours > threshold_hours:
            print(f"{employee_name} has worked for more than {threshold_hours} hours in a single shift.")
    else:
        print("no worker has worked more than 14 hours for single shift")
        

# Main function to execute the program
def main():
    file_path = 'Assignment_Timecard.xlsx - Sheet1.csv' 
    data = read_csv(file_path)

    # Call the functions to perform analyses and print results
    find_consecutive_days(data)
    find_short_shifts(data)
    find_long_shifts(data)

# Entry point of the program
if __name__ == "__main__":
    main()
