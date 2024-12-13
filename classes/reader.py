import time
from classes.person import Person

class Reader(Person):
    """
    A registered reader who can borrow books from the library
    """
    def __init__(self, name, last_name, dob, client_card_no:str, status:int = 1, added_user_id = "u-999"):
        super().__init__(name, last_name, dob, added_user_id)
        self.client_card_no = client_card_no
        
        self.status:int = status    # 1 - active, 2 - not active
        self.id:str = f"c-{str(int(time.time() * 100))}"     # c - client
        
    def __str__(self):
        return (
            f"[{self.id}, "
            f"{self.name}, "
            f"{self.last_name}, "
            f"{self.dob}, "
            f"{self.client_card_no}, "
            f"{self.status}, "
            f"{self.added_user_id}]"
        )
    
    def __repr__(self):    
        return (
            f"{self.__class__.__name__}("
            f"{self.id}, "
            f"{self.name}, "
            f"{self.last_name}, "
            f"{self.dob}, "
            f"{self.client_card_no}, "
            f"{self.status}, "
            f"{self.added_user_id}"
        )