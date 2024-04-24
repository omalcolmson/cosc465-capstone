import os
'''
Script just for reorganizing all of the Traceroute Output files
'''

def createFolders():
    parentFolder = "TracerouteOutputDevTool/"
    outputFolder = "DevToolTraceRoute/"
    for filename in os.listdir(parentFolder):
        ogdomain = filename[:filename.find(".txt")] #parse out the original domain used with devtool tracking
        # oldFile = open(f"{parentFolder}{filename}")
        subDir = f"{ogdomain}" #make a sub directory for each ogdomain
        path = os.path.join(outputFolder, subDir) 
        if not os.path.exists(path):
            os.makedirs(path)

def find_domain(line: str) -> str:
    start = line.find("to ") + 3 #add three to account for 'to '
    end = line.find(" (") 
    return line[start:end]



def separate_output():
    parentFolder = "TracerouteOutputDevTool/"
    outputFolder = "DevToolTraceRoute/"
    print("Separating traceroute output...")
    for filename in os.listdir(parentFolder):
        print(f"Working on {filename}...")
        ogdomain = filename[:filename.find(".txt")]
        oldFile = open(f"{parentFolder}{filename}", "r")
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
