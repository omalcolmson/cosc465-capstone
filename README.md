# COSC465 Capstone | Do You Know How Far Your Data Goes? – Following Network Traffic of Sites Commonly Used by Colgate Students
TEAM MEMBERS: Amanda Anowi, Carl Ekholm, Olivia Malcolmson, and Nyah Harrison

## Introduction
<p>Anytime you access the internet, information travels far and wide. But do you know just how far? A semester of studying computer networks demystifies the amorphous entity that is the internet and provides us with the knowledge and tools to track just how far your data travels. The scope of our project began within 22 domains that we collecitvely decided as a group to use as a representative sample of domains frequently visited by Colgate students -- we refer to these as our <span style="color:red"><em>original</em></span> domains. However, traversing the internet is rarely ever a direct flight, typically making multiple stops along the way and receiving support from other entities to retrieve relevant information -- some of these secondary entities are CDNs and/or ASes, but we generally refer to these as <span style="color:red"><em>supporting</em></span> domains.</p>   

<p>The following document serves to outline our research project and process, specifically focusing on the scripts we used to gather and prepare our data. We also have some archived scripts which we will describe briefly as they were used only for organizing our data.</p>


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