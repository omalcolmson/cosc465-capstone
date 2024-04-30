'''
Script for processing raw browser history data

Disclaimer:
When it came to my (Olivia's) browser history, I just exported my data to a csv file. I had trouble restricting my data to specific dates, so I just exported everything. This means that there could be sites that are included and were used more frequently on specific days rather than are typical sites I use on a day-to-day basis. 
'''
import pandas as pd


# def tldToDF(tldTxt: str) -> pd.DataFrame:
#     df = pd.read_csv(tldTxt)

#     return df

# def getTLD(url: str, tlds: pd.DataFrame) -> str:
#     '''Returns the TLD of a given URL by checking a TLD dataframe'''
#     tld = ""
#     return tld


def processURL(url:str) -> str:
    '''
    processes a url and gets rid of some unnecessary data to extract the generic domain of the url
    
    '''
    processed = ''
    prefixes = ['http://', 'https://', 'www.']
    for prefix in prefixes:
        if url.startswith(prefix):
            url = url.split(prefix)[1] #not sure if this should be kept
            # print(url)
            break
    slash = url.find('/') 
    processed = url[:slash] #not sure if we risk losing a lot of data here 
    # print(processed)

    return processed


def processBrowserHistory(csvpath: str):
    '''
    Takes in raw csv file path and rewrites to a new CSV, eliminating any unneccesary data
    '''
    df = pd.read_csv(csvpath)
    df.drop(columns=['DateTime', 'PageTitle'], inplace=True) #get rid of unnecessary columns of data
    df['NavigatedToUrl'] = df['NavigatedToUrl']
    
    # print(df.head(10))
    # for url in df['NavigatedToUrl']: #iterate through the rows of the URLs
    #     url = processURL(url)
    df['NavigatedToUrl'] = df['NavigatedToUrl'].apply(processURL)
    # group df by the urls and count occurrences of each
    counts = df.groupby(['NavigatedToUrl']).size().reset_index(name='Count')
    counts = counts[counts['Count'] > 1]
    counts = counts.sort_values(by='Count', ascending=False)
    # print(counts.head(11))
    counts.to_csv('OliviaData/MalcolmsonTopDomains.csv', index=False)

def main():
    processBrowserHistory("OliviaData/MalcolmsonBrowserHistory.csv")
    # tldsDF = tldToDF('tlds.txt') # can't remember why i thought I was going to use this
    # processURL('https://www.youtube.com/watch?v=sQcQEIkd2tw') #for testing

if __name__ == "__main__":
    main()