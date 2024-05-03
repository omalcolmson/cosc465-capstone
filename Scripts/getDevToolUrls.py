import json
import os

def getUrls(har_file_path, output_folder):

    os.makedirs(output_folder, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(har_file_path))[0] + '.txt'
    output_file_path = os.path.join(output_folder, base_name)
    
    with open(har_file_path, 'r') as file:
        har_data = json.load(file)
    
    with open(output_file_path, 'w') as output_file:
        entries = har_data['log']['entries']
        for entry in entries:
            url = entry['request']['url']
            output_file.write(url + '\n')

har_files = [
    'DevToolData/amazon.com.har',
    'DevToolData/buff.163.com.har',
    'DevToolData/chat.openai.com.har',
    'DevToolData/colgate.edu.har',
    'DevToolData/di.se.har',
    'DevToolData/dineoncampus.com.har',
    'DevToolData/docs.google.com.har',
    'DevToolData/drive.google.com.har',
    'DevToolData/github.com.har',
    'DevToolData/gmail.com.har',
    'DevToolData/google.com.har',
    'DevToolData/gradescope.com.har',
    'DevToolData/instagram.com.har',
    'DevToolData/linkedin.com.har',
    'DevToolData/moodle.colgate.edu.har',
    'DevToolData/netflix.com.har',
    'DevToolData/notion.so.har',
    'DevToolData/open.spotify.com.har',
    'DevToolData/pandas.pydata.org.har',
    'DevToolData/portal.colgate.edu.har',
    'DevToolData/x.com.har',
    'DevToolData/youtube.com.har',
]
output_folder = 'DevToolDataURLs'

for har_file in har_files:
    getUrls(har_file, output_folder)
