import requests
import csv
import os
from datetime import datetime
import sys  # Importamos sys para usar sys.exit()

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

# Main function to control the flow of the program
def main():
    # Get the current year to use in the file name
    current_year = datetime.now().year
    # Read the current IP from the file if it exists
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
