from classes.item import Item

class Book(Item):
    """
    A book item
    """
    def __init__(self, title, author, publication_year, genre, total_units, available_units, status:int = 1, added_user_id = "u-999"):
        super().__init__(title, author, publication_year, genre, total_units, available_units, status, added_user_id)
    
