from datetime import datetime
N_YEARCITATIONRANGE = 5

class Paper:
    def __init__(self, title, first_author, author_count, year, bibcode, citations):
        self.title = title
        self.first_author = first_author
        self.year = int(year)
        self.author_count = int(author_count)
        self.citations = citations if citations is not None else []
        self.bibcode = bibcode 
    
    def __str__(self):
        return(
            f"Title: {self.title}\n"
            f"First Author: {self.first_author}\n"
            f"Year: {self.year}\n"
            f"Author Count: {self.author_count}"
            f"Citation Count: {self.author_count}"
            f"Bibcode: {self.bibcode}\n"
        )
    
    @property
    def citation_count(self):
        return len(self.citations)
    
    @property
    def citation_count_five(self):
        if len(self.citations) == 0:
            return 0
        return sum(
            1 for c in self.citations
            if 'year' in c and c['year'] <= self.year +  N_YEARCITATIONRANGE
        )
    


    