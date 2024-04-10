import os
import re

# Function to extract domain names and IP addresses from trace route files
def extract_domains_and_ips(trace_route_folder):
    domain_ip_map = {}
    for file_name in os.listdir(trace_route_folder):
        if file_name.endswith('.txt'):
            with open(os.path.join(trace_route_folder, file_name), 'r') as file:
                for line in file:
                    ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
                    domain_match = re.search(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b', line)
                    if ip_match and domain_match:
                        ip_address = ip_match.group()
                        domain = domain_match.group()
                        domain_ip_map[domain] = ip_address
    return domain_ip_map

# Example usage:
trace_route_folder = 'TracerouteOutput'  
domain_ip_map = extract_domains_and_ips(trace_route_folder)

# Print extracted domain names and IP addresses
for domain, ip_address in domain_ip_map.items():
    print(f'{domain}: {ip_address}')
