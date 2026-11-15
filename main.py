"""IP Address Information Tool.

Displays the computer's current public IPv4 and IPv6 addresses together with
geolocation, ISP and ASN details.

How it works:
    1. ipify returns the public IPv4 / IPv6 address (get_ip).
    2. ipapi.co returns details about that address (get_ip_information).
    3. display_information prints one formatted section per IP version.

Setup and run:
    pip install -r requirements.txt
    python main.py

To continue the project, see the README for where to add features.
"""

import requests

# ---------------------------------------------------------------------------
# API endpoints
# To switch providers, change these constants (and the field names read in
# display_information if the new API uses different JSON keys).
# ---------------------------------------------------------------------------
IPV4_API = "https://api.ipify.org?format=json"    # returns {"ip": "<IPv4>"}
IPV6_API = "https://api6.ipify.org?format=json"   # returns {"ip": "<IPv6>"}; fails on IPv4-only networks
IP_INFO_API = "https://ipapi.co/{}/json/"         # {} is replaced with the IP address


def get_ip(url):
    """Retrieve the public IP address.

    Args:
        url (str): ipify endpoint to query (IPV4_API or IPV6_API).

    Returns:
        str | None: the IP address, or None if the request failed
        (no connection, timeout, HTTP error, or no IPv6 on this network).
    """
    try:
        # timeout stops the program from hanging if the API never answers
        response = requests.get(url, timeout=10)
        # raise an exception for HTTP errors such as 404 or 429
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException:
        # Return None instead of crashing; display_information reports it
        return None


def get_ip_information(ip):
    """Retrieve geolocation and ISP information.

    Args:
        ip (str): the IPv4 or IPv6 address to look up.

    Returns:
        dict | None: parsed JSON from ipapi.co, or None if the lookup failed
        (for example, when the free-tier rate limit is reached).
    """
    try:
        response = requests.get(
            IP_INFO_API.format(ip), timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def display_information(ip, version):
    """Display information for an IP address.

    Args:
        ip (str | None): address returned by get_ip, or None if unavailable.
        version (str): label for the report heading, "IPv4" or "IPv6".
    """

    print(f"\n===== {version} INFORMATION =====")

    # Case 1: the address itself could not be retrieved
    if not ip:
        print(f"{version} address unavailable.")
        return

    print(f"IP Address: {ip}")

    info = get_ip_information(ip)

    # Case 2: we have the address but the detail lookup failed
    if not info:
        print("Additional information unavailable.")
        return

    # .get() with "N/A" keeps the report working if the API omits a field.
    # To show a new field, add one print line here using its JSON key.
    print(f"Country: {info.get('country_name', 'N/A')}")
    print(f"Country Code: {info.get('country_code', 'N/A')}")
    print(f"City: {info.get('city', 'N/A')}")
    print(f"Region: {info.get('region', 'N/A')}")
    print(f"ISP: {info.get('org', 'N/A')}")
    print(f"ASN: {info.get('asn', 'N/A')}")
    print(f"Latitude: {info.get('latitude', 'N/A')}")
    print(f"Longitude: {info.get('longitude', 'N/A')}")


def main():
    """Run the program: fetch both public IPs and print one report each."""
    print("====================================")
    print("       IP ADDRESS INFORMATION")
    print("====================================")

    # Fetch both addresses first; either may be None
    ipv4 = get_ip(IPV4_API)
    ipv6 = get_ip(IPV6_API)

    display_information(ipv4, "IPv4")
    display_information(ipv6, "IPv6")

    print("\n====================================")
    print("          END OF REPORT")
    print("====================================")


# Only run main() when executed directly (python main.py),
# not when imported by another module or by tests.
if __name__ == "__main__":
    main()
