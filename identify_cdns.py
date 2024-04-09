from argparse import ArgumentParser
import os
import re

def parse_cdn_domains(filepath):
    """Parse CDN domains from traceroute output file"""
    cdn_domains = set()
    with open(filepath, 'r') as file:
        for line in file:
            # Regular expression to match CDN domains
            cdn_regex = r"((cdn|content-delivery-network|edge)\d*\.([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})"
            matches = re.findall(cdn_regex, line)
            for match in matches:
                cdn_domain = match[0]
                cdn_domains.add(cdn_domain)
    return list(cdn_domains)

def main():
    arg_parser = ArgumentParser(description='Parse CDN domains from traceroute output')
    arg_parser.add_argument('-d', '--directory', dest='directory', action='store',
                            required=True, help='Directory containing traceroute output files')
    arg_parser.add_argument('-o', '--output', dest='output', action='store',
                            required=True, help='Output file to save CDN domains')
    settings = arg_parser.parse_args()

    output_dir = settings.directory
    output_file = settings.output

    cdn_domains_dict = {}

    traceroute_output_dir = os.path.join(output_dir, 'TracerouteOutput')

    for filename in os.listdir(traceroute_output_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(traceroute_output_dir, filename)
            cdn_domains = parse_cdn_domains(filepath)
            if cdn_domains:
                cdn_domains_dict[filename] = cdn_domains

    with open(output_file, 'w') as f:
        for filename, cdn_domains in cdn_domains_dict.items():
            f.write("CDN domains found in {}: \n".format(filename))
            for domain in cdn_domains:
                f.write(domain + '\n')

    print("CDN domains written to {}".format(output_file))

if __name__ == '__main__':
    main()
