# Knowledge Hub Monitoring

## Project Description

This repository contains the initial Python monitoring configuration
application for Case Study 1 – The Knowledge Hub.

The application allows a user to configure a server for future
infrastructure monitoring.

## Requirements

- Python 3.12 or newer
- Git
- Windows or Linux

No additional Python packages are required.

## How to Run

1. Clone this repository.
2. Open the repository folder in a terminal.
3. Run:

   python monitoring_config.py

4. Enter the server hostname.
5. Enter a valid IP address.
6. Enter the monitoring metrics.
7. Type `done` to finish.

## Features

- Collects a server hostname.
- Validates IPv4 and IPv6 addresses.
- Collects multiple monitoring metrics.
- Prevents duplicate metrics.
- Rejects empty inputs.
- Stores the configuration temporarily in memory.
- Displays the completed configuration.

## Example Configuration

Hostname: KH-FS01

IP Address: 192.168.10.20

Metrics:
- CPU
- RAM
- Disk

## Task 5 — Original Limitations

This is an initial configuration application.

It does not yet:
- Collect live performance metrics.
- Save configurations to a database or file.
- Send notifications.
- Monitor server availability automatically.

These features may be developed in later tasks.

## Repository Structure

- monitoring_config.py – Main configuration application
- experiments/ – Earlier Python experiments
- README.md – Project documentation
- .gitignore – Files excluded from Git

## Testing

The application was manually tested using valid and invalid input.

Tests included:
- Empty hostname
- Invalid IP address
- Valid IP address
- Empty monitoring metric
- Duplicate metrics
- Multiple valid metrics
- Correct configuration output

## Task 10 — Infrastructure Monitoring

### Overview

In Task 10, I expanded my Python monitoring application from Task 5.

The application can now collect CPU, memory, and disk usage, save measurements to a CSV file, and retrieve previously stored measurements.

The application runs through PowerShell without asking the user for input during execution.

### Requirements

- Python 3.12 or newer
- psutil 6.1.1

Install the dependency using:

`python -m pip install psutil==6.1.1`

### Collect measurements

Run the following command:

`python monitoring.py collect --metrics cpu memory disk`

The application measures the selected metrics and saves the results to `measurements.csv`.

Each measurement contains a timestamp, hostname, metric name, value, and unit.

### View monitoring history

Retrieve measurements for a specific date:

`python monitoring.py report --start 2026-11-22 --end 2026-11-22`

Retrieve measurements for a specific time period:

`python monitoring.py report --start 2026-11-22T21:00 --end 2026-11-22T22:00`

The application reads the existing CSV file and displays measurements recorded during the selected period. Times are interpreted as UTC when no timezone is supplied.

### Data storage

Measurements are saved in `measurements.csv`.

The application appends new measurements instead of overwriting previous data.

The CSV file is excluded from GitHub using `.gitignore`.

### Testing

I tested the following functionality:

- Collecting CPU, memory, and disk measurements.
- Saving measurements to CSV.
- Running collection multiple times without overwriting existing data.
- Reading historical measurements.
- Filtering measurements by date and time.
- Rejecting unsupported metrics such as `temperature`.
- Rejecting date ranges where the start is after the end.
- Displaying a message when no measurements exist for the selected period.

These tests passed.

### Limitations

The application currently monitors only the computer running the script.

It collects measurements once per command execution rather than continuously.

The application uses CSV storage. In Task 11, I will extend it to use a local SQLite database.

The application does not currently send alerts or notifications.

## Task 11 — SQLite Monitoring Database

### Overview

In Task 11, I extended my Python monitoring application from Task 10 by replacing CSV storage with a local SQLite database.

The application still collects CPU, memory, and disk measurements using `psutil`. Measurements are now stored in `monitoring.db` instead of `measurements.csv`.

### Database Implementation

I created `database.py` to manage the SQLite database using Python's built-in `sqlite3` module.

The application uses three functions:

- `create_database()` — creates the database table if it does not exist.
- `save_measurements()` — adds new measurements to the database.
- `load_measurements()` — retrieves stored measurements.

Each record contains a unique ID, timestamp, hostname, metric name, measurement value, and unit.

### How to Run

Collect measurements:

`python monitoring.py collect --metrics cpu memory disk`

Retrieve historical measurements:

`python monitoring.py report --start 2026-11-22 --end 2026-11-22`

Retrieve measurements for a specific time period:

`python monitoring.py report --start 2026-11-22T22:00 --end 2026-11-22T23:00`

Times without a timezone are interpreted as UTC.

### Testing

I tested the following:

- Creating the SQLite database.
- Saving CPU, memory, and disk measurements.
- Reading existing database records.
- Running collection multiple times without overwriting data.
- Retrieving measurements by date.
- Rejecting unsupported metrics.
- Rejecting invalid date ranges.
- Handling periods without measurements.
- Verifying that invalid commands do not change existing records.

All tests passed. The database contained nine records after the tests.

### Data Protection

The `monitoring.db` file is excluded from Git using `.gitignore`.

The original Task 10 CSV file remains available locally, but the Task 11 application now reads and writes SQLite.

### Limitations

The application currently monitors the local computer only.

Measurements are collected once per execution rather than continuously.

Historical reports retrieve records from the SQLite database and filter them in Python. This works for a small project, but a database query would be more efficient for larger datasets.

The application does not currently provide automatic alerts or notifications.