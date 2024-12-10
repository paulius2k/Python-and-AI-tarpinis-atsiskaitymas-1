from classes.Item import Item

class Book(Item):
    """
    A book item
    """
    def __init__(self, title, author, publication_year, genre, total_units, available_units):
        super().__init__(title, author, publication_year, genre, total_units, available_units)
    
