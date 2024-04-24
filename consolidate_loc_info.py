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
    # print(df.head(10))
    temp = df.groupby(['Domain', 'City']).size().reset_index(name='Count')
    # print(temp.head(20))
    locCount = pd.merge(df, temp, on=['Domain', 'City'], how='left')
    locCount = locCount.drop_duplicates()

    locCount.to_csv('DomainLocCount.csv', index=False)

def main():
    simplify_devtools('devtool_geolocations.csv')
    simplify_geolocs('geolocations.csv')

if __name__ == '__main__':
    main()