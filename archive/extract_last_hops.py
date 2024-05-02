import os
import re

def extract_target_domains_and_ips(input_folder, output_filename):
    # Regular expression to match the target domain and IP address in the first line of each traceroute file
    pattern = re.compile(r'traceroute to ([\w\.-]+) \(([\d\.]+)\)')

    # Dictionary to store domains and their IPs
    domain_ip_map = {}

    # Iterate over each file in the specified directory
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder, file_name)
            with open(file_path, 'r') as file:
                first_line = file.readline()  # Read only the first line of each file
                match = pattern.search(first_line)
                if match:
                    domain = match.group(1)
                    ip = match.group(2)
                    domain_ip_map[domain] = ip  # Map domain to its IP

    # Write the extracted domain and IP information to the output file
    with open(output_filename, 'w') as file:
        for domain, ip in domain_ip_map.items():
            file.write(f'{domain} ({ip})\n')


input_folder = 'TracerouteOutput'  
output_filename = 'traceroute output extracted last hops'  
extract_target_domains_and_ips(input_folder, output_filename)
