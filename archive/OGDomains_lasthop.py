import os
import re
import csv

def extract_domain_last_hop(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        if lines[0].startswith('traceroute'):
            domain = re.search(r'to\s(.*?)\s\(', lines[0]).group(1)
            for line in reversed(lines):
                last_hop_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                if last_hop_match:
                    last_hop_ip = last_hop_match.group()
                    return domain, last_hop_ip
    return None, None

def main():
    input_directory = 'TracerouteOutput'
    output_file = 'lasthops_ogdomains.csv'

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Filename', 'Domain', 'Last_Hop_IP']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for filename in os.listdir(input_directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(input_directory, filename)
                domain, last_hop_ip = extract_domain_last_hop(filepath)
                if domain and last_hop_ip:
                    writer.writerow({'Filename': filename, 'Domain': domain, 'Last_Hop_IP': last_hop_ip})
                else:
                    print(f"Failed to extract domain and last hop IP from {filename}")

if __name__ == "__main__":
    main()
