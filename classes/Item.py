import time
from datetime import datetime
from modules.utilities import Database

class Item:
    """
    Any item that the library owns (e.g. a book, a magazine or other/)
    """

    def __init__(self, title:str, author:str, publication_year:int, genre:str, total_units:int, available_units:int, id:str = None, type:int = 1, status:int = 1, added_user_id:str = "u-999") -> None:
        self.title:str = title
        self.author:str = author
        self.publication_year:int = publication_year
        self.genre:str = genre
        self.type:int = type        # 1 - book, 2 - magazine
        self.total_units:int = total_units
        self.available_units:int = available_units
        self.status:int = status    # 1 - active, 2 - marked as deleted
        self.added_user_id:str = added_user_id

        if id:
            self.id = id
        else:
            self.id:str = f"i-{str(int(time.time() * 100))}"     # i - item
        
        self.ts_added:datetime = datetime.today()
   
    def __str__(self):
        return (
            f"[{self.id}, "
            f"{self.title}, "
            f"{self.author}, "
            f"{self.publication_year}, "
            f"{self.genre}, "
            f"{self.total_units}, "
            f"{self.available_units}, "
            f"{self.added_user_id}]"
        )
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.title}, {self.author}, {self.publication_year}, {self.genre}, {self.total_units}, {self.available_units}, {self.status}, {self.added_user_id}, {self.ts_added})"

    def save(self):
        # open MySQL db connection
        conn = Database.get_connection()
        cur = conn.cursor()

        # create tables if they don't exist
        # create ITEMS table (parent)
        cur.execute("""
                CREATE TABLE IF Not Exists `library_db`.`items` (
                `id` varchar(45) NOT NULL,
                `title` varchar(45) NOT NULL,
                `author` varchar(45) NOT NULL,
                `publication_year` int NOT NULL,
                `genre` varchar(45) NOT NULL,
                `type` int NOT NULL,       
                `total_units` int NOT NULL,
                `available_units` int NOT NULL,
                `status` int NOT NULL,
                `added_user_id` varchar(45) DEFAULT NULL,
                `ts_added` datetime DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE KEY `id_UNIQUE` (`id`) /*!80000 INVISIBLE */
                )
                """
            )
        conn.commit()
      
        # add entry to ITEMS table
        cur.execute("""
            INSERT INTO items (id, title, author, publication_year, genre, type, total_units, available_units, status, added_user_id, ts_added)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.id, self.title, self.author, self.publication_year, self.genre, self.type, self.total_units, self.available_units, self.status, self.added_user_id, self.ts_added)
        )
        conn.commit()
                
        conn.close()

    
    