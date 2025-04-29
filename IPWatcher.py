import requests
import csv
import os
import sys
from datetime import datetime, timedelta
import argparse  # Para manejar parámetros de línea de comandos

# Function to get the public IP and ASN information
def get_public_ip_and_asn():
    try:
        # Try to get the public IP address
        ip_response = requests.get('https://api.ipify.org')
        ip = ip_response.text
        
        # Try to get ASN and other details using the IP address
        asn_response = requests.get(f'https://ipinfo.io/{ip}/json')
        data = asn_response.json()
        asn = data.get('org', 'N/A')  # ASN is usually in 'org' field, e.g., "AS12345"
        
        return ip, asn
    except requests.RequestException:
        print("Error obtaining the public IP or ASN. No internet connection.")
        sys.exit()  # Exit the program if there's no internet connection

# Function to save the log into a CSV file
def save_log(ip, asn, year, start_date, end_date):
    # Ensure the CSV file is named correctly with the current year
    file_name = f"ip_log_{year}.csv"
    
    # Check if the file already exists
    if os.path.exists(file_name):
        # If it exists, open it in append mode
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([start_date, end_date, ip, asn])
    else:
        # If it doesn't exist, create it and write the header
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Start Date", "End Date", "Public IP", "ASN"])
            writer.writerow([start_date, end_date, ip, asn])

# Function to search for IPs on a given date (supporting intermediate ranges)
def search_ip_by_date(date):
    current_year = datetime.now().year
    file_name = f"ip_log_{current_year}.csv"
    
    if os.path.exists(file_name):
        found = False
        # Convert the given date string to a datetime object
        search_date = datetime.strptime(date, "%Y-%m-%d")
        
        # Define the start and end of the day (00:00:00 to 23:59:59)
        start_of_day = search_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = search_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                start_date_str = row[0].strip()
                end_date_str = row[1].strip()
                ip = row[2].strip()
                asn = row[3].strip()
                
                # Parse dates for comparison
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
                if end_date_str:
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
                else:
                    end_date = None  # No end date means the IP is still active
                
                # Check if the search date is in the range of start_date and end_date
                # 1. The search date is after or equal to the start date
                # 2. The search date is before or equal to the end date (if end date exists)
                if (start_date <= end_of_day and end_date is None) or \
                        (start_date <= end_of_day and (end_date is None or end_date >= start_of_day)):
                    # We also need to check if the end of this range intersects with the search date
                    if (start_date <= end_of_day and start_date >= start_of_day) or \
                       (end_date and end_date <= end_of_day and end_date >= start_of_day):
                        print(f"IP: {ip}, ASN: {asn}, Start Date: {start_date_str}, End Date: {end_date_str}")
                        found = True
        
        if not found:
            print(f"No IP found for the date: {date}")
    else:
        print("Log file not found.")

# Function to search for all records of a specific IP
def search_ip(ip_search):
    current_year = datetime.now().year
    file_name = f"ip_log_{current_year}.csv"
    
    if os.path.exists(file_name):
        found = False
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                start_date_str = row[0].strip()
                end_date_str = row[1].strip()
                ip = row[2].strip()
                asn = row[3].strip()
                
                if ip_search == ip:
                    print(f"IP: {ip}, ASN: {asn}, Start Date: {start_date_str}, End Date: {end_date_str}")
                    found = True
        
        if not found:
            print(f"No records found for IP: {ip_search}")
    else:
        print("Log file not found.")

# Main function to control the flow of the program
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="IP Logger with Date Search Functionality")
    parser.add_argument('--search-date', type=str, help="Search for IP on a specific date (format: YYYY-MM-DD)")
    parser.add_argument('--search-ip', type=str, help="Search for all records of a specific IP")
    
    args = parser.parse_args()
    
    # If search-date parameter is provided, perform the search by date
    if args.search_date:
        search_ip_by_date(args.search_date)
        return  # End the execution here if we are searching by date
    
    # If search-ip parameter is provided, perform the search by IP
    if args.search_ip:
        search_ip(args.search_ip)
        return  # End the execution here if we are searching by IP
    
    # If no search parameters, continue with regular IP logging
    current_year = datetime.now().year
    last_ip = None
    file_name = f"ip_log_{current_year}.csv"
    last_start_date = None
    last_end_date = None
    last_asn = None

    # If the file exists, read the last registered IP and ASN
    if os.path.exists(file_name):
        with open(file_name, mode='r') as file:
            lines = file.readlines()
            if len(lines) > 1:
                last_entry = lines[-1].split(',')
                last_start_date = last_entry[0].strip()
                last_end_date = last_entry[1].strip()
                last_ip = last_entry[2].strip()
                last_asn = last_entry[3].strip()

    # Get the current public IP and ASN
    current_ip, current_asn = get_public_ip_and_asn()
    
    if current_ip:
        # Get the current date and time
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # If the IP has changed, save it in the file
        if current_ip != last_ip or current_asn != last_asn:
            print(f"IP changed: {current_ip}, ASN: {current_asn}")
            if last_ip:  # If there's a previous IP, mark the previous end date
                save_log(last_ip, last_asn, current_year, last_start_date, current_date)
            last_start_date = current_date  # New start date for the new IP
            last_end_date = None  # The end date is not known yet for the current IP
            save_log(current_ip, current_asn, current_year, last_start_date, last_end_date)
        else:
            print("IP and ASN have not changed.")
    else:
        print("Unable to obtain the public IP and ASN.")

if __name__ == "__main__":
    main()
