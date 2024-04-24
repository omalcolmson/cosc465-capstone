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

    locCount.to_csv('DevToolLocCount.csv', index=False)
    # print(locCount.head(10))
    
    # print(df.head(10))

def simplify_geolocs(fname: str):
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
    # simplify_devtools('devtool_geolocations.csv')
    # simplify_geolocs('geolocations.csv')
    fname1 = 'DevToolLocCount.csv'
    fname2 = 'DomainLocCount.csv'
    output = 'LocationAnalysis.txt'
    df1 = pd.read_csv(fname1)
    # print(df1.head(10))
    df1.drop(columns=['Domain'], inplace=True)
    df1Count = df1.groupby(['City', 'State', 'Country']).sum().reset_index()
    df1Count.to_csv('DevToolLocTotals.csv')

    df2 = pd.read_csv(fname2)
    df2.drop(columns=['Domain'], inplace=True)
    df2Count = df2.groupby(['City', 'State', 'Country']).sum().reset_index()
    df2Count.to_csv('OGDomainsLocTotals.csv')
    # df1Count = pd.merge(df1, temp, on=['City', 'State', 'Country'], how='left')
    # print(temp.head(10))
    # with open(output, 'w') as file:
    #     df = pd.read_csv(fname1)
    #     file.write("Location Data from DevTool Domains")
        

if __name__ == '__main__':
    main()