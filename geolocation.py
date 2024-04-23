import requests
from collections import Counter

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data


print(get_location())

location_counts = {}
with open("geolocations.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        location = line.split(",")[2].strip()  # Extracting location from each line
        if location in location_counts:
            location_counts[location] += 1
        else:
            location_counts[location] = 1

# Sorting locations by count in descending order
sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)

# Writing the top 10 most common locations and their counts to a new file
with open("top_locations.txt", "w") as output_file:
    output_file.write("Top 10 Most Common Locations:\n")
    for location, count in sorted_locations[:10]:
        output_file.write(f"{location}: {count}\n")

# Writing all unique locations and their counts to a new file
with open("unique_locations.txt", "w") as output_file:
    output_file.write("All Unique Locations and Their Counts:\n")
    for location, count in sorted_locations:
        output_file.write(f"{location}: {count}\n")