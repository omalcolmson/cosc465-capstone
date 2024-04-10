import os
import re

# extract CDN domains from traceroute files
def extract_cdn_domains(trace_route_folder):
    cdn_domains = set()

    for file_name in os.listdir(trace_route_folder):
        if file_name.endswith('.txt'):
            with open(os.path.join(trace_route_folder, file_name), 'r') as file:
                for line in file:
                    domain_match = re.search(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b', line)
                    if domain_match:
                        domain = domain_match.group()
                        if "cdn" in domain.lower():
                            cdn_domains.add(domain)
    return cdn_domains

# print
trace_route_folder = 'TracerouteOutput'  
cdn_domains = extract_cdn_domains(trace_route_folder)

# Print extracted CDN domains
print("CDN Domains:")
for domain in cdn_domains:
    print(domain)
