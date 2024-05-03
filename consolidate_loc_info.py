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

def clean_format(fname: str):
    df = pd.read_csv(fname)
    for index, row in df.iterrows():
        # clean Domain column
        domaintxt = df.at[index, 'OGDomain'].strip()
        domaintxt = domaintxt[(domaintxt.find(':')+2):] #isolate only the domain
        txt = domaintxt.find("txt") #check if its a filename and remove the txt part
        if txt != -1:
            domaintxt = domaintxt[:txt-1]
        df.at[index, 'OGDomain'] = domaintxt

        #clean the IPAddr column
        ip = df.at[index, 'IPAddr'].strip()
        ip = ip[ip.find(':')+2:] #isolate just the addr and get rid of the 'IP: ' part
        df.at[index, 'IPAddr'] = ip

        #clean the City column
        citytxt = df.at[index, 'City'].strip()
        citytxt = citytxt[citytxt.find(':')+2:]
        df.at[index, 'City'] = citytxt

        #clean the state column
        df.at[index, 'State'] = df.at[index, 'State'].strip()

        #clean the country 
        df.at[index, 'Country'] = df.at[index, 'Country'].strip()
    
    df.to_csv(fname, index=False)


def get_totals(fname: str):
    '''
    Writes to a new CSV file with the total counts of all unique locations by city/state. 
    '''
    df = pd.read_csv(fname)
    df.drop(columns=['OGDomain', 'IPAddr'], inplace=True)
    cities = df.groupby(['City', 'State', 'Country']).size().reset_index(name='Count')
    cities.to_csv(f"intermediate_citycount.csv")
    # cities.to_csv(f"endserver_citycount.csv")

def totals_country(fname: str):
    df = pd.read_csv(fname)
    df.drop(columns=['City', 'State'], inplace=True)
    countries = df.groupby(['Country']).size().reset_index(name='Count')
    countries.to_csv('intermediate_countrycount.csv')
    # countries.to_csv('endserver_countrycount.csv')

def main():

    # get_totals('EndServersLocations.csv')
    # get_totals('IntermediateServerLocations.csv')

    # totals_country('EndServersLocations.csv')
    totals_country('IntermediateServerLocations.csv')

    # created a merged CSV with end server data
    # og_endservers = pd.read_csv('OriginalDomainEndServerLocs.csv')
    # support_endservers = pd.read_csv('DevToolDomainEndServerLocs.csv')
    # support_endservers.drop(columns='SupportingDomain', inplace=True)
    # merged_endservers = pd.concat([og_endservers, support_endservers], axis=0)
    # merged_endservers.to_csv('EndServersLocations.csv', index=True)

    #creating a merged CSV with intermediate server data
    # og_inter = pd.read_csv('OriginalDomainNONEndServerLocs.csv')
    # support_inter = pd.read_csv('DevToolDomainNONEndServerLocs.csv')
    # support_inter.drop(columns='SupportingDomain', inplace=True)
    # merged_inter = pd.concat([og_inter, support_inter], axis=0)
    # merged_inter.to_csv('IntermediateServerLocations.csv', index=True)

    # cleaning up the formatting of the information in the csv files
    # clean_format('EndServersLocations.csv')
    # clean_format('IntermediateServerLocations.csv')


    # added an index column back
    # merged_endservers = pd.read_csv('EndServersLocations.csv')
    # merged_inter = pd.read_csv('IntermediateServerLocations.csv')

    # merged_endservers.reset_index(inplace=True, drop=False)
    # merged_inter.reset_index(inplace=True, drop=False)

    # merged_endservers.to_csv('EndServersLocations.csv', index=False)
    # merged_inter.to_csv('IntermediateServerLocations.csv', index=False)

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
    pass        

if __name__ == '__main__':
    main()