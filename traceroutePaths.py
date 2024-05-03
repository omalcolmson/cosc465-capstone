#!/usr/bin/env python3
'''
Script for running paris-traceroute on list of domains in topdomains.csv
(code based on COSC465-L, lab 6)
'''
from argparse import ArgumentParser

import pandas as pd
import subprocess #for automating the script
import os

def main():

    df = pd.read_csv('RawData/topdomains.csv')
    urls = df['URL'].to_list()
    output_dir = 'TracerouteOutput'
    # print(urls)
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