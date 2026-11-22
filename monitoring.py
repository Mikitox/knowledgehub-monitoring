
"""Knowledge Hub Monitoring - Task 10."""

import argparse
import csv
import socket
from datetime import date, datetime, timezone
from pathlib import Path

import psutil

from monitoring_config import validate_metrics


# The file where measurements are saved.
DATA_FILE = "measurements.csv"

# Columns used in the CSV file.
COLUMNS = ["timestamp", "hostname", "metric", "value", "unit"]


def collect_metrics(metrics):
    """Measure CPU, memory and disk usage."""
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


def save_data(measurements):
    """Add new measurements without deleting old ones."""
    file_exists = Path(DATA_FILE).exists()

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)

        if not file_exists or Path(DATA_FILE).stat().st_size == 0:
            writer.writeheader()

        writer.writerows(measurements)



def show_history(start, end):
    """Show measurements between two UTC dates or times."""

    # Accept dates such as 2026-11-22
    # or times such as 2026-11-22T21:00.
    start_time = datetime.fromisoformat(start)
    end_time = datetime.fromisoformat(end)

    # A date-only end includes the entire day.
    if len(end) == 10:
        end_time = end_time.replace(
            hour=23, minute=59, second=59,
            microsecond=999999
        )

    # Treat times without a timezone as UTC.
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)

    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=timezone.utc)

    if start_time > end_time:
        raise ValueError("Start cannot be after end.")

    if not Path(DATA_FILE).exists():
        print("No saved measurements yet.")
        return

    found = False

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            measurement_time = datetime.fromisoformat(
                row["timestamp"]
            )

            if start_time <= measurement_time <= end_time:
                print(
                    f"{row['timestamp']} | "
                    f"{row['hostname']} | "
                    f"{row['metric']}: "
                    f"{row['value']}{row['unit']}"
                )
                found = True

    if not found:
        print("No measurements found for this period.")



def main():
    """Read commands entered in the terminal."""
    parser = argparse.ArgumentParser(
        description="Knowledge Hub Monitoring"
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    collect = commands.add_parser("collect")
    collect.add_argument("--metrics", nargs="+", required=True)

    report = commands.add_parser("report")
    report.add_argument("--start", required=True)
    report.add_argument("--end", required=True)

    args = parser.parse_args()

    try:
        if args.command == "collect":
            measurements = collect_metrics(args.metrics)
            save_data(measurements)

            print("Measurements saved successfully!")

            for item in measurements:
                print(
                    f"{item['metric']}: "
                    f"{item['value']}{item['unit']}"
                )

        elif args.command == "report":
            print("=== Monitoring History ===")
            show_history(args.start, args.end)

    except ValueError as error:
        parser.error(str(error))

    except OSError as error:
        parser.error(f"File or system error: {error}")


if __name__ == "__main__":
    main()
