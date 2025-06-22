import requests
import random
from paper import Paper
import pandas as pd
from datetime import datetime
import time

N = 300 # amount of papers per sample
YEAR_BEG = 1999
N_YEARCITATIONRANGE = 5

# Load your ADS API token
with open('ads-key.txt', 'r') as file:
    token = file.read().strip()

headers = {
    'Authorization': f'Bearer {token}'
}

df = pd.DataFrame(columns=['Title','Year','First Author','Author Count','Citation Count','Citation Five Years', 'Bibcode'])
currentyear = datetime.now().year
yearend = currentyear - N_YEARCITATIONRANGE - 1

start_time = time.time()
for year in range(YEAR_BEG,yearend+1):
    search_url = 'https://api.adsabs.harvard.edu/v1/search/query'
    search_params = {
        'q': f'year:{year} AND bibstem:ApJ',
        'fl': 'bibcode,author,title',
        'rows': 1000,
        'sort': 'date desc'
    }

    response = requests.get(search_url, headers=headers, params=search_params)
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 86400))
        print(f"Rate limit hit. Sleeping for {retry_after} seconds...")
        time.sleep(retry_after)
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            # just take everything and run
            df.to_csv(f'ApJPapers_{YEAR_BEG}-{currentyear-1}-{N}.csv',index=False)
            print('JSON decode failure. Backing up collected data so far')
            break
    else:
        df.to_csv(f'ApJPapers_{YEAR_BEG}-{currentyear-1}-{N}.csv',index=False)
        print(f'API status code {response.status_code}. Backing up collected data so far')
        break

    docs = data.get('response', {}).get('docs', [])
    if not docs:
        print(f"No papers found for {year}.")
        exit()


    rand_articles = random.sample(docs,N)
    for random_paper in rand_articles:
        bibcode = random_paper['bibcode']
        title = random_paper.get('title', [''])[0]
        authors = random_paper.get('author', [])
        first_author = authors[0]
        author_count = len(authors)

        # fetch cited papers
        citations_url = 'https://api.adsabs.harvard.edu/v1/search/query'
        citation_params = {
            'q': f'citations({bibcode})',
            'fl': 'bibcode,year',
            'rows': 2000
        }

        cite_response = requests.get(citations_url, headers=headers, params=citation_params)

        if cite_response.status_code == 200:
            try:
                cite_data = cite_response.json()
            except ValueError:
                # just take everything and run
                df.to_csv(f'ApJPapers_{YEAR_BEG}-{currentyear-1}-{N}.csv',index=False)
                print('JSON decode failure. Backing up collected data so far')
                break
        else:
            df.to_csv(f'ApJPapers_{YEAR_BEG}-{currentyear-1}-{N}.csv',index=False)
            print(f'API status code {response.status_code}. Backing up collected data so far')
            break

        citing_docs = cite_data.get('response', {}).get('docs', [])
        citations = [{'bibcode': doc['bibcode'], 'year':int(doc.get('year'))} for doc in citing_docs]

        paper = Paper(title,first_author,author_count,year,bibcode,citations)
        
        paper_df = pd.DataFrame([{
            'Title': paper.title,
            'Year': paper.year,
            'First Author': paper.first_author,
            'Author Count': paper.author_count,
            'Citation Count': paper.citation_count,
            'Citation Five Years': paper.citation_count_five,
            'Bibcode': paper.bibcode
        }])

        df = pd.concat([df,paper_df],ignore_index=True)

    print(df)

df.to_csv(f'ApJPapers_{YEAR_BEG}-{yearend}-{N}.csv',index=False)
end_time = time.time()
print(f'Execution time: {end_time - start_time}')
