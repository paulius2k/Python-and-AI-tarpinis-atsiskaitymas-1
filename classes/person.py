from datetime import datetime

class Person:
    """A person, a parent class for Reader and Librarian"""
    
    def __init__(self, name:str, last_name:str, dob:datetime, added_user_id:str = "u-999") -> None:
        self.name:str = name
        self.last_name:str = last_name
        self.dob:int = dob
        
        self.added_user_id:str = added_user_id
        self.ts_added:datetime = datetime.today()
        
