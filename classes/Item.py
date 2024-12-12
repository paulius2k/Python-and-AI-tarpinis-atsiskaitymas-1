import random
from datetime import datetime

class Item:
    """
    Any item that the library owns (e.g. a book /or in the future - a magazine or other/)
    """
    
    def __init__(self, title:str, author:str, publication_year:int, genre:str, total_units:int, available_units:int, status:int = 1, added_user_id:str = "u-999") -> None:
        self.title:str = title
        self.author:str = author
        self.publication_year:int = publication_year
        self.genre:str = genre
        self.total_units:int = total_units
        self.available_units:int = available_units
        self.status:int = status    # 1 - active, 2 - deleted
        self.added_user_id:str = added_user_id

        self.id:str = f"i-{str(random.randint(100000,999999))}"
        self.ts_added:datetime = datetime.today()
   
    def __str__(self):
        return (
            f"{self.id}, "
            f"{self.title}, "
            f"{self.author}, "
            f"{self.publication_year}, "
            f"{self.genre}, "
            f"{self.total_units}, "
            f"{self.available_units}, "
            f"{self.added_user_id}, "
        )
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.title}, {self.author}, {self.publication_year}, {self.genre}, {self.total_units}, {self.available_units}, {self.status}, {self.added_user_id})"

    
    