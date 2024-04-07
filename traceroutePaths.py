#!/usr/bin/env python3
# script for running paris-traceroute and analyzing the output
# (copied from COSC465-L, lab 6)
from argparse import ArgumentParser
import socket
import time
import requests 
import ipaddress
import pandas as pd
import subprocess #for automating the script
import os

#TODO: Modify script so we can automate the process of running paris-traceroute on a list of domains

def parse_file(filepath):
    """Parses a file containing output from paris-traceroute and returns a 
    list of router addresses
    """
    with open(filepath) as datafile:
        lines = datafile.readlines()

    datalines = lines[1:-1]
    path = [parse_line(line) for line in datalines]
    path = [node for node in path if node != None]
    return path

def parse_line(line):
    """Parses a single line of output from paris-traceroute"""
    # Ensure it is a hop line
    line = line.strip()
    if line.startswith("MPLS"):
        return None
   
    # Break line into parts 
    parts = line.split(' ')
    parts = [part for part in parts if part !='']
    hostname = parts[1]
    ip = parts[2].strip('()')

    # Return hostname and IP address
    if hostname == ip:
        hostname = None
    if ip == "*":
        return None
    return (ip, hostname)

def get_entity(jsonResponse: dict) -> str:
    ASName = ''
    for k, v in jsonResponse.items(): #for every k,v in the outer response dict
        if k == 'entities': #find the key for entities
            # print(v)
            # print()
            # print()
            for items in v: #item is a dictionary
                if items.get('roles') != None and 'registrant' in items.get('roles'):
                    ASName = items.get('vcardArray')[1][1][-1]
                    # print(ASName)
    return ASName

def get_ASes(hops):
    """Converts a list of (Internet Protocol address, hostname) tuples to a list of (autonomous system number, autonomous system name) tuples"""
    # should pass in path (output of parse_file)
    ASes = []
    ipr1 = ipaddress.IPv4Network('10.0.0.0/8')
    ipr2 = ipaddress.IPv4Network('172.16.0.0/12')
    ipr3 = ipaddress.IPv4Network('192.168.0.0/16')
    # TODO
    for pair in hops: #iterates by tuples in the list hops
        # print(pair)
        ip = pair[0]
        if (ipaddress.IPv4Address(ip) not in ipr1) and (ipaddress.IPv4Address(ip) not in ipr2) and (ipaddress.IPv4Address(ip) not in ipr3): # if the ip is NOT private, continue
            try: 
                r = requests.get('https://rdap.arin.net/registry/ip/'+ip) #issues the request
                time.sleep(2) #enforce 2 queries per second
                try:
                    # print(type(r.json()))
                    ASes.append(get_entity(r.json()))
                except requests.exceptions.JSONDecodeError:
                    print("Error! Response contains no content!")
            except ConnectionError:
                print("Connection Error!")
            except TimeoutError:
                print("Request timed out!") 

    return list(set(ASes))

def summarize_path(hops):
    """Output IP, hostnames, and ASes in path"""
    print("Routers ({})".format(len(hops)))
    print('\t' + '\n\t'.join(["{}\t{}".format(ip, ("" if hostname is None else hostname)) for ip, hostname in hops]))
    ases = get_ASes(hops)
    print("ASes ({})".format(len(ases)))
    print('\t' + '\n\t'.join(["{}\t{}".format(asn, name) for asn, name in ases])) 

def main():
    # Parse arguments
    # arg_parser = ArgumentParser(description='Analyze Internet path')
    # arg_parser.add_argument('-f', '--filepath', dest='filepath', action='store',
    #         required=True, 
    #         help='Path to file with paris-traceroute output')
    # settings = arg_parser.parse_args()

    # path = parse_file(settings.filepath)
    # summarize_path(path)
    # nyuPaths = parse_file('nyu.txt')
    df = pd.read_csv('RawData/topdomains.csv')
    urls = df['URL'].to_list()
    output_dir = 'TracerouteOutput'

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        # commandList = f"./docker_traceroute.sh {url} > /TracerouteOutput/{url}.txt".split()
        output_file = os.path.join(output_dir, f'{url}.txt')
        commandList = ['./docker_traceroute.sh', url]
        try: 
            with open(output_file, 'w') as outfile:
                subprocess.run(commandList, stdout=outfile, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running traceroute for domain {url}: {e}")
    
    # print(get_ASes(path))

if __name__ == '__main__':
    main()