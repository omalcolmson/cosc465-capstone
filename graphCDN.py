import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv("cdn_counts.csv")

# Sort the DataFrame by count in descending order
df_sorted = df.sort_values(by='Count', ascending=False)

# Plot the CDN counts as a bar chart
plt.figure(figsize=(10, 6))
plt.bar(df_sorted['CDN'], df_sorted['Count'], color='skyblue')
plt.xlabel('CDN')
plt.ylabel('Count')
plt.title('CDN Counts')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the plot to an output file
plt.savefig('cdn_counts_bar_chart.png')
plt.show()
