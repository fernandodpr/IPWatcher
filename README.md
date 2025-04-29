
# IPWatcher

IPWatcher is a simple Python script that tracks your public IP address and logs it into a CSV file whenever it changes. It does not require any API registration, and it will monitor and log your connection's identity with timestamps for future reference.

## Features
- Tracks public IP address changes.
- Logs IP address with timestamps in a CSV file.
- No API registration required.
- Supports searching logs by date or IP address.
- Logs ASN (Autonomous System Number) and associated information for the IP.
  
## Installation

To use IPWatcher, follow the instructions below.

### Prerequisites
- Python 3.x installed on your machine.
- Required Python libraries: `requests`.

You can install the required dependencies using `pip`:

```bash
pip install requests
```

### Usage

Run the script to log your public IP address:

```bash
python3 IPWatcher.py
```

#### Search Logs by Date

To search for logs of IP addresses on a specific date:

```bash
python3 IPWatcher.py --search-date YYYY-MM-DD
```

#### Search Logs by IP Address

To search for all logs that contain a specific IP address:

```bash
python3 IPWatcher.py --search-ip YOUR_IP_ADDRESS
```

### Automating the Script with Cron

You can set up a cron job to run the script automatically every 2 minutes (or any other interval).

#### Steps:
1. Open your crontab file by typing the following command in your terminal:

```bash
crontab -e
```

2. Add the following line to run the script every 2 minutes:

```bash
*/2 * * * * /usr/bin/python3 /path/to/your/IPWatcher.py
```

Make sure to replace `/path/to/your/IPWatcher.py` with the full path to the `IPWatcher.py` script on your system.

#### Save and exit the crontab file. 

The script will now run every 2 minutes and will log the IP address if it changes.

### Log File Format

The log file will be saved with the name `ip_log_YYYY.csv` where `YYYY` is the current year. Each entry contains:

- Start Date (timestamp of the IP change).
- End Date (timestamp when the IP was replaced or a new one was assigned).
- Public IP Address.
- ASN (Autonomous System Number) and associated network details.

Example log entry:

```
Start Date, End Date, IP Address, ASN
2025-04-15 12:45:00, 2025-04-20 18:00:00, 198.51.100.100, AS64501 ExampleNet-2
```

## License

This project is open-source and available under the [MIT License](LICENSE).
