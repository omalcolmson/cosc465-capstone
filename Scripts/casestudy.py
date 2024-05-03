from collections import Counter

# Define a dictionary to store the count of domains for each city
city_domain_count = Counter()

# Extracted data from the logs
data = [
    {"Original Domain": "dineoncampus.com", "Location": "Secaucus, New Jersey, US"},
    {"Original Domain": "dineoncampus.com", "Location": "San Francisco, California, US"},
    {"Original Domain": "dineoncampus.com", "Location": "Secaucus, New Jersey, US"},
    {"Original Domain": "dineoncampus.com", "Location": "New York City, New York, US"},
    # Add more data here
]

# Count the number of domains for each city
for entry in data:
    location = entry["Location"]
    city_domain_count[location] += 1

# Find the most popular city
most_popular_city, count = city_domain_count.most_common(1)[0]

print("Most popular city for dineoncampus.com:", most_popular_city)
print("Number of different domains traversed in the most popular city:", count)
