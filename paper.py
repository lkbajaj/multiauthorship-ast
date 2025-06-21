class Paper:
    def __init__(self, title, first_author, author_count, year, bibcode, citation_count):
        self.title = title
        self.first_author = first_author
        self.year = year
        self.author_count = author_count
        self.citation_count = citation_count
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
    