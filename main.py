
import requests

# ==========================================
# TERMINAL COLORS
# ==========================================

RESET = "\033[0m"
BOLD = "\033[1m"

CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
GRAY = "\033[90m"

IPV4_API = "https://api.ipify.org?format=json"
IPV6_API = "https://api6.ipify.org?format=json"
IP_INFO_API = "https://ipapi.co/{}/json/"

def get_ip(url):
    """Retrieve the public IP address."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["ip"]
    except (requests.RequestException, KeyError, ValueError):
        return None

def get_ip_information(ip):
    """Retrieve geolocation and ISP information."""
    try:
        response = requests.get(
            IP_INFO_API.format(ip), timeout=10
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def display_header():
    print()
    print(CYAN + BOLD + "=" * 55 + RESET)
    print(CYAN + BOLD + "             IP ADDRESS INFORMATION" + RESET)
    print(CYAN + BOLD + "=" * 55 + RESET)
    print()


def display_section_title(version):
    print()
    print(BLUE + BOLD + "-" * 55 + RESET)
    print(WHITE + BOLD + f"  {version} NETWORK INFORMATION" + RESET)
    print(BLUE + BOLD + "-" * 55 + RESET)


def display_information(ip, version):
    """Display IP address and its corresponding information."""

    display_section_title(version)

    if not ip:
        print(RED + "  Address unavailable." + RESET)
        return

    print(GREEN + "  Address retrieved successfully." + RESET)
    print()
    print(CYAN + BOLD + "  IP Address" + RESET)
    print(WHITE + f"  {ip}" + RESET)

    info = get_ip_information(ip)

    if not info:
        print()
        print(YELLOW + "  Additional information unavailable." + RESET)
        return

    print()
    print(CYAN + BOLD + "  LOCATION INFORMATION" + RESET)
    print(GRAY + "  " + "-" * 35 + RESET)

    print(f"  Country       : {info.get('country_name') or 'N/A'}")
    print(f"  Country Code  : {info.get('country_code') or 'N/A'}")
    print(f"  City          : {info.get('city') or 'N/A'}")
    print(f"  Region        : {info.get('region') or 'N/A'}")

    print()
    print(CYAN + BOLD + "  NETWORK INFORMATION" + RESET)
    print(GRAY + "  " + "-" * 35 + RESET)

    print(f"  ISP           : {info.get('org') or 'N/A'}")
    print(f"  ASN           : {info.get('asn') or 'N/A'}")

    print()
    print(CYAN + BOLD + "  GEOGRAPHIC COORDINATES" + RESET)
    print(GRAY + "  " + "-" * 35 + RESET)

    print(f"  Latitude      : {info.get('latitude') or 'N/A'}")
    print(f"  Longitude     : {info.get('longitude') or 'N/A'}")


def main():

    display_header()

    print(YELLOW + "  Retrieving IP address information..." + RESET)

    ipv4 = get_ip(IPV4_API)
    ipv6 = get_ip(IPV6_API)

    display_information(ipv4, "IPv4")
    display_information(ipv6, "IPv6")

    # Footer
    print()
    print(CYAN + BOLD + "=" * 55 + RESET)
    print(GREEN + BOLD + "               REPORT COMPLETED" + RESET)
    print(CYAN + BOLD + "=" * 55 + RESET)
    print(GRAY + "       IPv4 / IPv6 Address Application" + RESET)
    print()


if __name__ == "__main__":
    main()