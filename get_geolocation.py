import os
import re
import requests

# regex pattern for ip 
ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

# extract IP addresses from a traceroute file
def extract_ips(filename) -> list:
    '''
    Returns a list of IP addresses from an entire file
    '''
    ips = []
    with open(filename, 'r') as file:
        endServer = ''
        for line in file:
            ip_match = ip_pattern.search(line)
            if 'traceroute' in line: #then we know we're looking at the first line that contains that ip of the end server
                # print("end server:", ip_match.group())
                endServer = ip_match.group()
            if ip_match:
                # check if the ip is the end server - if it is and it hasn't been added yet, we can add it
                if ip_match.group() == endServer and endServer not in ips: #avoid double counting the ip addr of the end server for a given traceroute file
                    ips.append(ip_match.group())
                elif ip_match.group() != endServer: # else if it's not the end server, then we can add 
                    ips.append(ip_match.group())
    return ips

# get geolocation of an IP using ipinfo.io
def get_geolocation(ip) -> str:
    '''
    Queries for the geolocation of a given IP address and returns the location in a string formatted by {city}, {region}, {country}
    '''
    try:
        response = requests.get(f"http://ipinfo.io/{ip}?token=efbefc0f3bee64")
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
    folder_path = "TracerouteOutput"
    output_file = "geolocations.csv"
    
    # rerunning this on the newly updated devtool traceroute stuff
    # folder_path = "TracerouteOutputDevTool"
    # output_file = "devtool_geolocations.txt"

    with open(output_file, 'w') as output:
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                ips = extract_ips(file_path)
                # print(filename)
                # print(ips)
                if ips:
                    for ip in ips:
                        geolocation = get_geolocation(ip)
                        # print(geolocation)
                        if geolocation:
                            output.write(f"Domain: {filename}, IP: {ip}, Location: {geolocation}\n")
                        else:
                            output.write(f"Domain: {filename}, IP: {ip}, Location: Not found\n")

if __name__ == "__main__":
    main()
