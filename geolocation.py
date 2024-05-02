import requests
from collections import Counter

# Function to retrieve public IP address
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

# Function to retrieve location data for a given IP address
def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

# Function to process trace route output and extract geolocation data
def process_trace_route(filename):
    ip_addresses = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 2:
                hop_number, ip_address = parts[0], parts[1]
                ip_addresses.append(ip_address)
    
    # Retrieving geolocation data for each IP address
    locations = [get_location(ip) for ip in ip_addresses]
    return locations

# Getting geolocation for trace route output from DevToolTraceRoute2k
trace_route_file = "DevToolTraceRoute2k.txt"
trace_route_locations = process_trace_route(trace_route_file)

# Counting occurrences of each location
location_counts = Counter(location["country"] for location in trace_route_locations)

# Sorting locations by count in descending order
sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)

# Writing the top 10 most common locations and their counts to a new file
with open("top_locations_trace_route.txt", "w") as output_file:
    output_file.write("Top 10 Most Common Locations:\n")
    for location, count in sorted_locations[:10]:
        output_file.write(f"{location}: {count}\n")

# Writing all unique locations and their counts to a new file
with open("unique_locations_trace_route.txt", "w") as output_file:
    output_file.write("All Unique Locations and Their Counts:\n")
    for location, count in sorted_locations:
        output_file.write(f"{location}: {count}\n")

# Differentiating between last hops and intermediary hops
end_nodes = [location["country"] for location in trace_route_locations[-10:]]  # Assuming last 10 hops are end nodes
intermediary_nodes = [location["country"] for location in trace_route_locations[:-10]]

# Printing last hops and intermediary hops
print("Last Hops (End Nodes):", end_nodes)
print("Intermediary Hops (Routers):", intermediary_nodes)
