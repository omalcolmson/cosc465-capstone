import os
'''
Script just for reorganizing all of the Traceroute Output files.

Separates the traceroute output that was run on all supporting domains and originally compiled into a single file into separate files organized in folders sorted by original domains.

Before: 

amazon.com.txt -> 1 file with multiple traceroute output runs for multiple supporting domains

After: 
amazon.com -> Folder containing files where the traceroute output for each supporting domain has been separated
    aan.amazon.com.txt
    fls-na.amazon.com.txt
    ...
'''

def createFolders():
    '''
    Creates separate folders for each original domain where the individual txt files for each supporting domain will reside after being separated
    '''
    parentFolder = "TracerouteOutputDevTool/"
    outputFolder = "DevToolTraceRoute2k/"
    for filename in os.listdir(parentFolder):
        ogdomain = filename[:filename.find(".txt")] #parse out the original domain used with devtool tracking
        # oldFile = open(f"{parentFolder}{filename}")
        subDir = f"{ogdomain}" #make a sub directory for each ogdomain
        path = os.path.join(outputFolder, subDir) 
        if not os.path.exists(path):
            os.makedirs(path)

def find_domain(line: str) -> str:
    '''
    Extracts the original domain from the first line of the traceroute output

    line: str
        expected format: traceroute to buff.163.com (52.10.244.182), 30 hops max, 30 bytes packets

    '''
    start = line.find("to ") + 3 #add three to account for 'to '
    end = line.find(" (") 
    return line[start:end]

def separate_output():
    '''
    Iterates through each file in the parentfolder and creates a new file for each traceroute output of the supporting domains
    '''
    parentFolder = "TracerouteOutputDevTool/"
    outputFolder = "DevToolTraceRoute2k/"
    print("Separating traceroute output...")
    for filename in os.listdir(parentFolder):
        print(f"Working on {filename}...")
        ogdomain = filename[:filename.find(".txt")]
        with open(f"{parentFolder}{filename}", "r") as oldFile:
        # outputFile = open(f"{outputFolder}{ogdomain}", "w")
            aline = oldFile.readline()
            while aline: #while there are lines in the file
                if "traceroute to" in aline: #then we know it's the beginning of a separate traceroute run
                    extra = 0
                    domain = find_domain(aline)
                    outputFilePath = f"{outputFolder}{ogdomain}/{domain}.txt"
                    while os.path.exists(outputFilePath):
                        outputFilePath = f"{outputFolder}{ogdomain}/{domain}{extra+1}.txt"
                        extra += 1
                    print(f"Writing for {domain} which was tracked when querying for {ogdomain}...")
                    outputFile = open(outputFilePath, "w")
                    outputFile.write(aline)
                    aline = oldFile.readline()
                    while aline != '' and "traceroute to" not in aline:
                        outputFile.write(aline)
                        aline = oldFile.readline()

def main():
    # createFolders()
    # separate_output()
    pass
if __name__ == "__main__":
    main()
