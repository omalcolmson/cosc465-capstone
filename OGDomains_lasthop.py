import os
import re

def extract_domain_last_hop(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        domain = re.search(r'to\s(.*?)\s\(', lines[0]).group(1)
        for line in reversed(lines):
            last_hop_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if last_hop_match:
                last_hop_ip = last_hop_match.group()
                return domain, last_hop_ip
        return None, None

def main():
    input = 'TracerouteOutput'
    output_file = 'output.txt'

    with open(output_file, 'w') as output:
        for filename in os.listdir(input):
            if filename.endswith('.txt'):
                filepath = os.path.join(input, filename)
                domain, last_hop_ip = extract_domain_last_hop(filepath)
                if domain and last_hop_ip:
                    output.write(f'{domain}, {last_hop_ip}\n')
                else:
                    print(f"Failed to extract domain and last hop IP from {filename}")

if __name__ == "__main__":
    main()
