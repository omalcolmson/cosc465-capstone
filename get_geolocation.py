import os
import re
import requests

# regex pattern for ip 
ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

# extract IP addresses from a traceroute file
def extract_ips(filename):
    ips = []
    with open(filename, 'r') as file:
        for line in file:
            ip_match = ip_pattern.search(line)
            if ip_match:
                ips.append(ip_match.group())
    return ips

# get geolocation of an IP using ipinfo.io
def get_geolocation(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/json?token=c9c103e4f334e4")
        data = response.json()
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        return f"{city}, {region}, {country}"
    except Exception as e:
        print(f"Error fetching geolocation for IP {ip}: {e}")
        return None

def main():
    # For parsing traceroute output to list of ORIGINAL domains
    # folder_path = "TracerouteOutput"
    # output_file = "geolocations.txt"
    
    # For parsing traceroute output to list of additional domains that came up from tracking network activity via dev tools
    # Only first 5 for each original domain were sampled
    folder_path = "TracerouteOutputDevTool"
    output_file = "devtool_geolocations.txt"

    with open(output_file, 'w') as output:
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                ips = extract_ips(file_path)
                if ips:
                    for ip in ips:
                        geolocation = get_geolocation(ip)
                        if geolocation:
                            output.write(f"Domain: {filename}, IP: {ip}, Location: {geolocation}\n")
                        else:
                            output.write(f"Domain: {filename}, IP: {ip}, Location: Not found\n")

if __name__ == "__main__":
    main()
