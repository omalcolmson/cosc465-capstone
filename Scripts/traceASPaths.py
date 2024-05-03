#!/usr/bin/env python3
# script for analyzing traceroute output on a given domain
# (copied from COSC465-L, lab 6)

import socket
import time
import requests 
import ipaddress
import dns.resolver as ds
import pandas as pd
import GetDevToolCDNs as retriever #importing Amanda's functions to rerun AS retrieval on original domain names

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

def queryAS(ip: str, r: ds.Resolver) -> tuple:
    '''
    Queries the AS number for a given IP using Team Cymru's IP to ASN mapping service.
    The function reverses the IP address, appends the domain for Cymru's service, and performs a TXT DNS query.
    '''
    if ip is None:
        return (["-1"], ["Unknown"])
    
    reversed_ip = '.'.join(ip.split('.')[::-1])
    query_domain_asn = f"{reversed_ip}.origin.asn.cymru.com"
    
    try:
        response_asn = r.resolve(query_domain_asn, 'TXT')
        as_info = response_asn[0].to_text().strip('"').split(' | ')
        asn_list = as_info[0].split()
        as_names = []

        for asn in asn_list:
            query_domain_asname = f"AS{asn}.asn.cymru.com"
            response_asname = r.resolve(query_domain_asname, 'TXT')
            asname = response_asname[0].to_text().strip('"').split(' | ')[-1]
            as_names.append(asname)

        return asn_list
    except ds.NXDOMAIN:
        print("Query name does not exist!")
        return (["-1"], ["Unknown"])
    except ds.LifetimeTimeout:
        print("Query timed out!")
        return (["-1"], ["Unknown"])
    except Exception as e:
        return (["-1"], ["Unknown"])

def get_entity(jsonResponse: dict) -> tuple:

    r = ds.Resolver() #local
    r.nameservers = ['127.0.0.1'] #specified from example
    r.port = 8053 #assign the port to send from

    ASName = ''
    for k, v in jsonResponse.items(): #for every k,v in the outer response dict
        if k == 'entities': #find the key for entities
            # print(v)
            # print()
            # print()
            for items in v: #item is a dictionary
                if items.get('roles') != None and 'registrant' in items.get('roles'):
                    ASName = items.get('vcardArray')[1][1][-1]
                    ASipaddrlookup = items.get('links')[0]['value']
                    ASipaddr = ASipaddrlookup.split('ip/')[1]
                    ASN = queryAS(ASipaddr, r)[0]
                    # print(ASName)
    return (ASN, ASName)

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
                    asTuple = get_entity(r.json())
                    if asTuple not in ASes:
                        ASes.append(asTuple)
                except requests.exceptions.JSONDecodeError:
                    print("Error! Response contains no content!")
            except ConnectionError:
                print("Connection Error!")
            except TimeoutError:
                print("Request timed out!") 

    return ASes

def summarize_path(hops):
    """Output IP, hostnames, and ASes in path"""
    print("Routers ({})".format(len(hops)))
    print('\t' + '\n\t'.join(["{}\t{}".format(ip, ("" if hostname is None else hostname)) for ip, hostname in hops]))
    ases = get_ASes(hops)
    print("ASes ({})".format(len(ases)))
    print('\t' + '\n\t'.join(["{}\t{}".format(asn, name) for asn, name in ases])) 

def getASNames(path) -> list:
    '''
    "[('1289', 'Colgate University'), (['-1'], 'NYSERNet'), (['-1'], 'TELEHOUSE International Corp. of America')]"
    '''
    ASNames = []
    for pair in path:
        if pair[1] not in ASNames:
            ASNames.append(pair)
    return ASNames


def main():
    #for testing
    # amazonPath = parse_file("TracerouteOutput/google.com.txt")
    # # summarize_path(amazonPath)
    # print(get_ASes(amazonPath))

    # df = pd.read_csv("RawData/topdomains.csv")
    # df.drop(columns="Count", inplace=True)
    # df['IP'] = 0 #new column for number of AS orgs
    # df['ASName'] = ''# new column for list of ASes traversed
    # for index, row in df.iterrows():
    #     url = row['URL']
    #     fname = f'{url}.txt'
    #     # urlPath = parse_file(f'TracerouteOutput/{fname}')
    #     ip, as_names = retriever.extract_and_get_as_names(f'TracerouteOutput/{fname}')
    #     if ip and as_names:
    #         df.at[index, 'Domain'] = url
    #         df.at[index, 'IP'] = ip
    #         if len(as_names) == 1:
    #             df.at[index, 'ASName'] = as_names[0]
    #         else:
    #             as_names
        
    # df.to_csv("DomainsAnalysis.csv")
    # df = pd.read_csv('OGDomainsASes.csv')
    # df.drop(columns='Domain', inplace=True)
    # df.to_csv('OGDomainsASes.csv', index=False)

    # created merged CSV with all AS info
    # df1 = pd.read_csv('OGDomainsASes.csv')
    # df1.drop(columns='Index', inplace=True)
    # df2 = pd.read_csv('DevToolAses.csv')
    # merged = pd.concat([df1, df2], axis=0)
    # merged.to_csv('ASInfo.csv')

    ases = pd.read_csv('ASInfo.csv')
    ases.drop(columns=['Domain', 'IP'], inplace=True)
    counts = ases.groupby(['ASName']).size().reset_index(name='Count')
    counts.to_csv('AS_Counts.csv')

    # pass


if __name__ == '__main__':
    main()