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

## Current Limitations

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
