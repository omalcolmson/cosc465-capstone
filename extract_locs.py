import re
import os
import pandas as pd
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
            
    else: # if 1, so goes through devtool traceroute
        parentFolder = 'DevToolTraceRoute2k/'
        for childFolder in os.listdir(parentFolder):
            for fileName in os.listdir(f"{parentFolder}{childFolder}/"):
                with open(f"{parentFolder}{childFolder}/{fileName}", "r") as readFile:
                    firstLine = readFile.readline() #reads first line in the file
                    ip = find_ip(firstLine)
                    if ip != '':
                        servers.append(ip)

    return servers

def containsServer(line: str, servers: list) -> bool:
    '''
    Checks to see if any end servers are in this line
    '''
    for server in servers:
        if server in line:
            return True
    return False

def main():
    # list of end servers for the original 22 domains
    og_endservers = find_end_servers(0)
    # list of end servers for the supporting domains
    supporting_endservers = find_end_servers(1)

    '''
    Will use these lists of servers to extract out location data from the original CSV files of original and supporting domains
    to separate end and intermediate hops. 
    '''
    non_endservers = []
    # for original domains csv
    with open('OriginalDomainEndServerLocs.csv', 'w') as writeFile:
        with open('geolocations.csv', 'r') as readFile: #will read 

    # for supporting domains csv
    # with open('DevToolDomainEndServerLocs.csv', 'w') as writeFile:
    #     with open('devtool_geolocations2k.csv', 'r') as readFile: #will read 
            line = readFile.readline() #read the first line which is just the headers
            non_endservers.append(line)
            writeFile.write(line)
            line = readFile.readline() #now should read first line of actual data
            while line:
                # for server in og_endservers: #for every end server
                if containsServer(line, og_endservers):
                    writeFile.write(line) #write end server locations to new file
                else:
                    non_endservers.append(line) #append to a list we'll write to new file
                # for server in supporting_endservers: #for every end server
                #     if server in line: #check if end server is in this line
                #         writeFile.write(line) #write end server locations to new file
                #     else: #if it's not an end server
                #         if line not in non_endservers:
                #             non_endservers.append(line) #append to a list we'll write over the original file
                line = readFile.readline() #read next line after every server has been checked
            
    # when all lines have been read
    with open('OriginalDomainNONEndServerLocs.csv', 'w') as writeFile1:
    # with open('DevToolDomainNONEndServerLocs.csv', 'w') as writeFile1:
        writeFile1.writelines(non_endservers) #will write all the non-end servers back to this csv

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