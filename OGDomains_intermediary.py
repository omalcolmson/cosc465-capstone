import os
import re

def extract_intermediary_hops(filepath):
    intermediary_hops = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        first_ip = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', lines[1])
        if first_ip:
            first_ip = first_ip.group()
            for line in lines[2:]:  # Exclude the first line and everything after the last hop IP
                ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
                if ip_match:
                    ip = ip_match.group()
                    if ip != first_ip:  # Exclude the first IP if it appears again
                        intermediary_hops.append(ip)
    return intermediary_hops

def main():
    input_directory = 'TracerouteOutput'
    output_file = 'intermediary_hops_output.txt'

    with open(output_file, 'w') as output:
        for filename in os.listdir(input_directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(input_directory, filename)
                intermediary_hops = extract_intermediary_hops(filepath)
                output.write(f'{filename}:\n')
                for hop in intermediary_hops:
                    output.write(f'{hop}\n')
                output.write('\n')

if __name__ == "__main__":
    main()
