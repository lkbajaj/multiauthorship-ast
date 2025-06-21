import requests
import random
from paper import Paper
import pandas as pd

N = 300 # amount of papers per sample
YEAR_BEG = 1999
YEAR_END = 2024

# Load your ADS API token
with open('ads-key.txt', 'r') as file:
    token = file.read().strip()

headers = {
    'Authorization': f'Bearer {token}'
}

df = pd.DataFrame(columns=['Title','Year','First Author','Author Count','Citation Count', 'Bibcode'])
for year in range(YEAR_BEG,YEAR_END+1):
    search_url = 'https://api.adsabs.harvard.edu/v1/search/query'
    search_params = {
        'q': f'year:{year} AND bibstem:ApJ',
        'fl': 'bibcode,author,title,citation_count',
        'rows': 1000,
        'sort': 'date desc'
    }

    response = requests.get(search_url, headers=headers, params=search_params)
    data = response.json()

    docs = data.get('response', {}).get('docs', [])
    if not docs:
        print("No papers found for 2024.")
        exit()


    rand_articles = random.sample(docs,N)
    for random_paper in rand_articles:
        bibcode = random_paper['bibcode']
        title = random_paper.get('title', [''])[0]
        citation_count = random_paper.get('citation_count', 0)
        authors = random_paper.get('author', [])
        first_author = authors[0]
        author_count = len(authors)

        paper = Paper(title,first_author,author_count,year,bibcode,citation_count)
        
        paper_df = pd.DataFrame([{
            'Title': paper.title,
            'Year': paper.year,
            'First Author': paper.first_author,
            'Author Count': paper.author_count,
            'Citation Count': paper.citation_count,
            'Bibcode': paper.bibcode
        }])

        df = pd.concat([df,paper_df],ignore_index=True)
        print(df)

df.to_csv(f'ApJPapers_{YEAR_BEG}-{YEAR_END}-{N}.csv',index=False)
