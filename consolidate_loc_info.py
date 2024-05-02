import pandas as pd
'''
Script for consolidating all of our location data into counts that will be easier to graph and display visually.

This script will write to CSV files using a pandas DataFrame. 
'''

def simplify_devtools(fname: str):
    '''
    For simplifying the devtools geolocations csv, and organizing it into another csv that accumulates counts for the  
    '''
    df = pd.read_csv(fname, header=None)
    cols = ["Domain", "IPAddr", "City", "State", "Country"]
    df.columns = cols
    df.drop(columns="IPAddr", inplace=True)
    for index, row in df.iterrows(): #clean up the data
        domaintxt = df.at[index, 'Domain']
        domaintxt = domaintxt[(domaintxt.find(':')+2):(domaintxt.find("txt")-1)]
        df.at[index, 'Domain'] = domaintxt.strip()
        citytxt = df.at[index, 'City']
        citytxt = citytxt[citytxt.find(':')+2:]
        df.at[index, 'City'] = citytxt.strip()
        df.at[index, 'Country'] = df.at[index, 'Country'].strip()
        df.at[index, 'State'] = df.at[index, 'State'].strip()
    
    temp = df.groupby(['Domain', 'City']).size().reset_index(name='Count')
    # print(temp.head(20))
    locCount = pd.merge(df, temp, on=['Domain', 'City'], how='left')
    locCount = locCount.drop_duplicates()

    locCount.to_csv('DevToolLocCount2k.csv', index=False)
    # print(locCount.head(10))
    
    # print(df.head(10))

def simplify_geolocs(fname: str):
    '''
    For simplifying the original locations for the original domains
    '''
    df = pd.read_csv(fname)
    df.drop(columns="IPAddr", inplace=True)
    for index, row in df.iterrows(): #clean up the data
        domaintxt = df.at[index, 'Domain']
        domaintxt = domaintxt[(domaintxt.find(':')+2):(domaintxt.find("txt")-1)]
        df.at[index, 'Domain'] = domaintxt.strip()
        citytxt = df.at[index, 'City']
        citytxt = citytxt[citytxt.find(':')+2:]
        df.at[index, 'City'] = citytxt.strip()
        df.at[index, 'Country'] = df.at[index, 'Country'].strip()
        df.at[index, 'State'] = df.at[index, 'State'].strip()
    # print(df.head(10))
    temp = df.groupby(['Domain', 'City']).size().reset_index(name='Count')
    # print(temp.head(20))
    locCount = pd.merge(df, temp, on=['Domain', 'City'], how='left')
    locCount = locCount.drop_duplicates()

    locCount.to_csv('DomainLocCount.csv', index=False)

def main():
    # created a merged CSV with end server data
    # og_endservers = pd.read_csv('OriginalDomainEndServerLocs.csv')
    # support_endservers = pd.read_csv('DevToolDomainEndServerLocs.csv')
    # support_endservers.drop(columns='SupportingDomain', inplace=True)
    # merged_endservers = pd.concat([og_endservers, support_endservers], axis=0)
    # merged_endservers.to_csv('EndServersLocations.csv', index=False)

    #creating a merged CSV with intermediate server data
    og_inter = pd.read_csv('OriginalDomainNONEndServerLocs.csv')
    support_inter = pd.read_csv('DevToolDomainNONEndServerLocs.csv')
    support_inter.drop(columns='SupportingDomain', inplace=True)
    merged_inter = pd.concat([og_inter, support_inter], axis=0)
    merged_inter.to_csv('IntermediateServerLocations.csv', index=False)

    # simplify_devtools('devtool_geolocations2k.csv')
    # simplify_geolocs('geolocations.csv')
    # fname1 = 'DevToolLocCount2k.csv'
    # # fname2 = 'DomainLocCount.csv'
    # df1 = pd.read_csv(fname1)
    # # print(df1.head(10))
    # df1.drop(columns=['Domain'], inplace=True)
    # df1Count = df1.groupby(['City', 'State', 'Country']).sum().reset_index()
    # df1Count.to_csv('DevToolLocTotals2k.csv')

    # commenting og domain stuff as we are only rerunning on updated devtool output
    # df2 = pd.read_csv(fname2)
    # df2.drop(columns=['Domain'], inplace=True)
    # df2Count = df2.groupby(['City', 'State', 'Country']).sum().reset_index()
    # df2Count.to_csv('OGDomainsLocTotals.csv')
    # df1Count = pd.merge(df1, temp, on=['City', 'State', 'Country'], how='left')
    # print(temp.head(10))
    # with open(output, 'w') as file:
    #     df = pd.read_csv(fname1)
    #     file.write("Location Data from DevTool Domains")
        

if __name__ == '__main__':
    main()