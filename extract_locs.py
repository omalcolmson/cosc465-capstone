import re
import os
'''
Script for extracting the locations of all end servers and outputting them to a different CSV file to generate different counts for our graphs.
'''

def find_ip(line: str) -> str:
    '''
    Returns the ip address in a given string
    Will only be passed the first line of traceroute output files
    '''
    # regex pattern for ip 
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ip_match = ip_pattern.search(line)
    return ip_match.group() if ip_match != None else ''


def find_end_servers(indicator: int) -> list:
    '''
    Returns a list of end servers (ip addresses as strings) extracted from traceroute output
    
    indicator -> int for for parsing the original or supporting domains' traceroute output
        0: original domains' traceroute (files in TracerouteOutput)
        1: supporting domains' traceroute (files in folders of DevToolTraceRoute2k)
    '''
    servers = []
    parentFolder = '' #will change depending on indicator
    if indicator == 0: #for parsing files in TracerouteOutput
        parentFolder = 'TracerouteOutput/'
        for filename in os.listdir(parentFolder):
            with open(f"{parentFolder}{filename}", "r") as readFile:
                firstLine = readFile.readline() #reads first line in the file
                ip = find_ip(firstLine)
                if ip != '':
                    servers.append(ip)
            
    else: 
        parentFolder = 'DevToolTraceRoute2k/'
        for childFolder in os.listdir(parentFolder):
            for fileName in os.listdir(f"{parentFolder}{childFolder}/"):
                with open(f"{parentFolder}{childFolder}/{fileName}", "r") as readFile:
                    firstLine = readFile.readline() #reads first line in the file
                    ip = find_ip(firstLine)
                    if ip != '':
                        servers.append(ip)

    return servers

def main():
    # for some preliminary testing
    # og = find_end_servers(0)
    # print(og)
    # print(len(og)) #should be 22 for the 22 original domains
    # og = find_end_servers(1)
    # print(og)
    # print(len(og))
    pass
if __name__ == "__main__":
    main()