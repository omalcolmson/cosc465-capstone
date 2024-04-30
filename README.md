# COSC465 Capstone | Do You Know How Far Your Data Goes? – Following Network Traffic of Sites Commonly Used by Colgate Students
TEAM MEMBERS: Amanda Anowi, Carl Ekholm, Olivia Malcolmson, and Nyah Harrison

## Introduction
Anytime you access the internet, information travels far and wide. But do you know just how far? A semester of studying computer networks demystifies the amorphous entity that is the internet and provides us with the knowledge and tools to track just how far your data travels. The scope of our project began within 22 domains that we collecitvely decided as a group to use as a representative sample of domains frequently visited by Colgate students -- we refer to these as our *original* domains. However, traversing the internet is rarely ever a direct flight, typically making multiple stops along the way and receiving support from other entities to retrieve relevant information -- some of these secondary entities are CDNs and/or ASes, but we generally refer to these as *supporting* domains.

The following document serves to outline our research project and process, specifically focusing on the scripts we used to gather and prepare our data. We also have some archived scripts which we will describe briefly as they were used only for organizing our data.


### Breaking down the tasks
We wrote our scripts to achieve and support the following tasks:
- run `traceroute` on each of our original domains to examine intermediate nodes and end servers (supporting domains)
- use the internet browser developer tool to track the network activity when directly visiting the original domains to get a list of all supporting domains  
- determine the geographic location of these intermediate nodes and end servers via IP address lookups
- determine what, if any, AS organizations oversaw the routers and/or end servers that were part of the path taken to get to the origial domain

### Matching the Tasks and the Supporting Scripts
**`traceroutePaths.py`**
- iterates through the list of original domains and runs `traceroute-paris`, writing the output for each to a separate file
- output for each original domain is stored in the `TracerouteOutput` folder where the title of the file is the domain that was passed in to traceroute
- this was also used on all supporting domains gathered from the devtool tracking and the output for each of those supporting domains is stored in the `TracerouteOutputDevTool` folder where the title of the file is the *original* domain and the contents contain multiple traceroute outputs for the supporting domains (this was done on the initial 5 sampled)

**`traceASPaths.py`**
- iterates through each traceroute output file and parses the data to culminate information regarding the names and numbers of AS organizations found during the traversal
- outputs this data to `DomainsAnalysis.csv` for the original domains

**`traceroutepathsDevTool.py`**

This script iterates through topdomainsDev.txt and runs `traceroute-paris`, writing the output for each to a separate file. The outputs are stored in a different folder called TracerouteOutputDevTool and in this folder the name of each .txt file represents the domain that was passed into traceroute.


**`geolocation.py`**

[ insert explanation here]


**`get_geolocation.py`**

[ insert explanation here]


**`getCDN.py`**

[ insert explanation here]


**`getIPS.py`**

[ insert explanation here]


**`getDevToolUrls.py`**

When using the Developer Tool on Google Chrome you can download files from the Networks tab that contains all possible information of the domains that your orginal website queries. This script runs on those downloadable files in order to create .txt files of the urls that are in those files. 

<details>
<summary><strong> Archived Code Descriptions </strong></summary>
<blockquote><strong><code>devtoolorg.py</code></strong> 
<hr> Script for separating traceroute output of supporting domains that had originally been compiled into one txt file according to the original domain into separate txt files for each supporting domain organized by folders of the original domain they were supporting
</blockquote>
<br>
<p>For instance, all of the traceroute output for all supporting domains found via the devtool for chatGPT were in one file like so:</p>
                
    CONTENTS OF chatopenai.com.txt:
    traceroute to chat.openai.com (104.18.37.228), 30 hops max, 30 bytes packets
    1  172.17.0.1 (172.17.0.1)  0.067ms    0.064ms    0.054ms  
    ...

    traceroute to cdn.oaistatic.com (104.18.41.158), 30 hops max, 30 bytes packets
    1  172.17.0.1 (172.17.0.1)  0.045ms    0.040ms    0.035ms  
    ...
        
<p>But these were then separated into files under the same folder of the original domain they supported, following a structure more similar to the following:</p>

    -- /DevToolTraceRoute2k
        | -- chat.openai.com/
            | -- chat.openai.com.txt
            -- cdn.oaistatic.com.txt

<blockquote><strong><code>consolidate_loc_info.py</code></strong> 
<hr> Script for consolidating all location information into pandas dataframes and outputting the information to csv files with counts and totals we could use for graphs
</blockquote>

</details>
