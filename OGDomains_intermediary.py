import os
import re

def extract_intermediary_hops(filepath):
    intermediary_hops = []
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines[1:-1]:  # Exclude the first and last line
            ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if ip_match:
                intermediary_hops.append(ip_match.group())
    return intermediary_hops

def main():
    input_directory = 'TracerouteOutput'
    output_file = 'intermediary_ogdomains.txt'

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
