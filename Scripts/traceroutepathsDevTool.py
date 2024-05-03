#!/usr/bin/env python3
import subprocess
import os
from urllib.parse import urlparse

def read_domains_and_urls(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    domains = {}
    current_domain = None
    url_list = []  

    for line in lines:

        if not line.strip() or line.strip().lower() == 'url':
            continue

        '''  
        if 'https://' not in line:
            if current_domain:
                domains[current_domain] = url_list  
            current_domain = line.strip()  
            url_list = []  
        else:
            url_list.append(line.strip())'''
        
        #Need to handle http as well not only https

        if 'https://' in line or 'http://' in line:
            url_list.append(line.strip())
        else:
            if current_domain:
                domains[current_domain] = url_list
            current_domain = line.strip()
            url_list = []


    if current_domain and url_list:  
        domains[current_domain] = url_list

    return domains

def run_traceroute(domains, output_dir):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for domain, urls in domains.items():
        if domain: 
            output_file = os.path.join(output_dir, f'{domain}.txt')
            with open(output_file, 'w') as outfile:
                for url in urls:
                    parsed_url = urlparse(url)
                    hostname = parsed_url.hostname.replace('www.', '') if parsed_url.hostname else ''
                    if hostname:  
                        commandList = ['./docker_traceroute.sh', hostname]
                        try:
                            subprocess.run(commandList, stdout=outfile, check=True)
                        except subprocess.CalledProcessError as e:
                            print(f"Error running traceroute for domain {url}: {e}")

def main():
    file_path = 'RawData/topdomainsDev.txt'  
    domains = read_domains_and_urls(file_path)
    run_traceroute(domains, 'TracerouteOutputDevTool')

if __name__ == '__main__':
    main()
