import csv
from collections import Counter

def read_cdn_domains(file_path):
    cdn_domains = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            cdn = row[-1]  # Extract the CDN from the last column
            cdn_domains.append(cdn)
    return cdn_domains

def count_cdn_occurrences(cdn_domains):
    return Counter(cdn_domains)

def write_cdn_counts(cdn_counts, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CDN', 'Count'])
        for cdn, count in cdn_counts.items():
            writer.writerow([cdn, count])

def main():
    input_file = "DevToolCDNs.csv"
    output_file = "cdn_counts.csv"

    cdn_domains = read_cdn_domains(input_file)
    cdn_counts = count_cdn_occurrences(cdn_domains)
    write_cdn_counts(cdn_counts, output_file)

if __name__ == "__main__":
    main()
