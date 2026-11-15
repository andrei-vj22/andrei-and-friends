
import requests

# API endpoints
IPV4_API = "https://api.ipify.org?format=json"
IPV6_API = "https://api6.ipify.org?format=json"
IP_INFO_API = "https://ipapi.co/{}/json/"


def get_ip(url):
    """Retrieve the public IP address."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException:
        return None


def get_ip_information(ip):
    """Retrieve geolocation and ISP information."""
    try:
        response = requests.get(
            IP_INFO_API.format(ip), timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def display_information(ip, version):
    """Display information for an IP address."""

    print(f"\n===== {version} INFORMATION =====")

    if not ip:
        print(f"{version} address unavailable.")
        return

    print(f"IP Address: {ip}")

    info = get_ip_information(ip)

    if not info:
        print("Additional information unavailable.")
        return

    print(f"Country: {info.get('country_name', 'N/A')}")
    print(f"Country Code: {info.get('country_code', 'N/A')}")
    print(f"City: {info.get('city', 'N/A')}")
    print(f"Region: {info.get('region', 'N/A')}")
    print(f"ISP: {info.get('org', 'N/A')}")
    print(f"ASN: {info.get('asn', 'N/A')}")
    print(f"Latitude: {info.get('latitude', 'N/A')}")
    print(f"Longitude: {info.get('longitude', 'N/A')}")


def main():
    print("====================================")
    print("       IP ADDRESS INFORMATION")
    print("====================================")

    ipv4 = get_ip(IPV4_API)
    ipv6 = get_ip(IPV6_API)

    display_information(ipv4, "IPv4")
    display_information(ipv6, "IPv6")

    print("\n====================================")
    print("          END OF REPORT")
    print("====================================")


if __name__ == "__main__":
    main()
