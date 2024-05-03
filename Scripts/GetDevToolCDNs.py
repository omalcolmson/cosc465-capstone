import os
import re
import dns.resolver
import csv

# Define the patterns for IP extraction
ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

# DNS Resolver setup
r = dns.resolver.Resolver()
r.nameservers = ['127.0.0.1']
r.port = 8053

# List of CDN names
cdn_names = {
    "akamai",
    "amazon cloudfront",
    "Azure", 
    "CDN77",
    "cloudflarenet",
    "edgecast",
    "fastly",
    "gcore", 
    "google-cloud-platform",
    "imperva", 
    "liquidweb",
    "akamai-asn1",
    "akamai-as",
}

# Function to extract IP and get associated AS names
def extract_and_get_as_names(filename):
    with open(filename, 'r') as file:
        content = file.read()
        ip_match = ip_pattern.search(content)
        if ip_match:
            ip = ip_match.group()
            as_names = get_as_names(ip)
            return ip, as_names
    return None, None

# Function to perform WHOIS lookup for AS names
def get_as_names(ip):
    try:
        reversed_ip = '.'.join(reversed(ip.split('.')))
        query_as_info = f"{reversed_ip}.origin.asn.cymru.com"
        result = r.resolve(query_as_info, 'TXT')
        as_info = result[0].strings[0].decode('utf-8').split('|')
        ases = [f"AS{asn.strip()}" for asn in as_info[0].split()]
        as_names = []
        for asn in ases:
            as_name = get_as_name(asn)
            if as_name:
                as_names.append(as_name)
        return as_names
    except dns.resolver.NXDOMAIN:
        print(f"No ASN found for {ip}")
        return []

# Function to perform WHOIS lookup for AS name
def get_as_name(asn):
    try:
        query_asn = f"{asn}.asn.cymru.com"
        result = r.resolve(query_asn, 'TXT')
        as_info = result[0].strings[0].decode('utf-8').split('|')
        as_name = as_info[4].strip().split(',')[0]  # Extracting only the first part before comma
        return as_name
    except dns.resolver.NXDOMAIN:
        print(f"No AS name found for {asn}")
        return None

# Function to check if AS name is in CDN list
def is_cdn(as_name):
    return as_name.lower() in {cdn.lower() for cdn in cdn_names}

# Function to extract domain name from filename
def extract_domain(filename):
    return os.path.splitext(filename)[0]

# Main function
def main():
    output_file = "DevToolAses.csv"
    cdn_output_file = "DevToolCDNs.csv"
    parent_folder = "DevToolTraceRoute2k"

    with open(output_file, 'w', newline='') as output, open(cdn_output_file, 'w', newline='') as cdn_output:
        ases_writer = csv.writer(output)
        cdns_writer = csv.writer(cdn_output)
        ases_writer.writerow(['Domain', 'IP', 'AS Names'])
        cdns_writer.writerow(['Domain', 'IP', 'CDN'])

        for root, dirs, files in os.walk(parent_folder):
            for file in files:
                if file.endswith(".txt"):
                    print(file)
                    file_path = os.path.join(root, file)
                    domain_name = extract_domain(file)
                    ip, as_names = extract_and_get_as_names(file_path)
                    if ip and as_names:
                        ases_writer.writerow([domain_name, ip, ', '.join(as_names)])
                        for as_name in as_names:
                            if is_cdn(as_name.lower()):
                                cdns_writer.writerow([domain_name, ip, as_name])
                                break  # Exit the loop once a match is found

if __name__ == "__main__":
    main()
