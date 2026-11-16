
"""Initial monitoring configuration for the Knowledge Hub."""

import ipaddress


def get_hostname():
    """Ask for a non-empty server hostname."""
    while True:
        hostname = input("Enter server hostname: ").strip()

        if hostname:
            return hostname

        print("Hostname cannot be empty. Please try again.")


def get_ip_address():
    """Ask for a valid server IP address."""
    while True:
        ip_address = input("Enter server IP address: ").strip()

        try:
            ipaddress.ip_address(ip_address)
            return ip_address
        except ValueError:
            print("Invalid IP address. Please try again.")


def get_metrics():
    """Collect at least one unique monitoring metric."""
    metrics = []

    while True:
        metric = input(
            "Enter metric (or 'done' to finish): "
        ).strip()

        if metric.lower() == "done":
            if metrics:
                return metrics

            print("Please enter at least one metric.")

        elif not metric:
            print("Metric cannot be empty.")

        elif metric.casefold() in (
            existing.casefold() for existing in metrics
        ):
            print("This metric has already been added.")

        else:
            metrics.append(metric)


def main():
    """Collect and display the monitoring configuration."""
    print("=== Knowledge Hub Monitoring ===")

    configuration = {
        "hostname": get_hostname(),
        "ip_address": get_ip_address(),
        "metrics": get_metrics(),
    }

    print("\n=== Monitoring Configuration ===")
    print(f"Hostname: {configuration['hostname']}")
    print(f"IP Address: {configuration['ip_address']}")

    print("Metrics:")
    for metric in configuration["metrics"]:
        print(f"- {metric}")


if __name__ == "__main__":
    main()
