
"""Knowledge Hub Monitoring - Task 11."""

import argparse
import socket
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import psutil

from monitoring_config import validate_metrics
from database import save_measurements, load_measurements


def collect_metrics(metrics):
    """Collect CPU, memory and disk usage."""
    results = []
    hostname = socket.gethostname()

    for metric in validate_metrics(metrics):

        if metric == "cpu":
            value = psutil.cpu_percent(interval=1)

        elif metric == "memory":
            value = psutil.virtual_memory().percent

        elif metric == "disk":
            value = psutil.disk_usage(Path.home().anchor).percent

        results.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hostname": hostname,
            "metric": metric,
            "value": value,
            "unit": "%"
        })

    return results


def show_history(start, end):
    """Show measurements saved in SQLite for a time period."""

    start_time = datetime.fromisoformat(start)
    end_time = datetime.fromisoformat(end)

    # Include the entire end date if only a date is entered.
    if len(end) == 10:
        end_time = end_time.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999
        )

    # Use UTC when no timezone is provided.
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)

    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=timezone.utc)

    if start_time > end_time:
        raise ValueError("Start time cannot be after end time.")

    # Read measurements from SQLite.
    measurements = load_measurements()

    found = False

    for item in measurements:
        measurement_time = datetime.fromisoformat(
            item["timestamp"]
        )

        if start_time <= measurement_time <= end_time:
            print(
                f"{item['timestamp']} | "
                f"{item['hostname']} | "
                f"{item['metric']}: "
                f"{item['value']}{item['unit']}"
            )
            found = True

    if not found:
        print("No measurements found for this period.")


def main():
    """Run monitoring commands from the terminal."""

    parser = argparse.ArgumentParser(
        description="Knowledge Hub Monitoring"
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Command for collecting measurements.
    collect = commands.add_parser("collect")

    collect.add_argument(
        "--metrics",
        nargs="+",
        required=True
    )

    # Command for showing historical measurements.
    report = commands.add_parser("report")

    report.add_argument(
        "--start",
        required=True
    )

    report.add_argument(
        "--end",
        required=True
    )

    args = parser.parse_args()

    try:

        if args.command == "collect":

            measurements = collect_metrics(args.metrics)

            # Save the measurements to SQLite.
            save_measurements(measurements)

            print("Measurements saved to SQLite successfully!")

            for item in measurements:
                print(
                    f"{item['metric']}: "
                    f"{item['value']}{item['unit']}"
                )

        elif args.command == "report":

            print("=== Monitoring History (SQLite) ===")

            show_history(args.start, args.end)

    except ValueError as error:
        parser.error(str(error))

    except (OSError, sqlite3.Error) as error:
        parser.error(f"Storage or system error: {error}")


if __name__ == "__main__":
    main()
