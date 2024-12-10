import random

class Item:
    """
    Any item for loan that the library owns (a book, or in the future - a magazine or other)
    """
    
    def __init__(self, title, author, publication_year, genre, total_units, available_units) -> None:
        self.id = random.randint(0,999999999) 
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.genre = genre
        self.total_units = total_units
        self.available_units = available_units
        
    def __str__(self):
        pass
        

