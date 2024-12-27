import time
from classes.person import Person
from modules.utilities import Database

class Reader(Person):
    """
    A registered reader who can borrow books from the library
    """
    def __init__(self, personal_code, name, last_name, dob, client_card_no:str, id = None, status:int = 1, added_user_id = "u-999"):
        super().__init__(personal_code, name, last_name, dob, added_user_id)
        self.client_card_no = client_card_no      
        self.status:int = status    # 1 - active, 2 - not active
        if id:
            self.id = id
        else:
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
        
    def save(self):
        # open MySQL db connection
        conn = Database.get_connection()
        cur = conn.cursor()

        # create tables if they don't exist
        # create PERSONS table (parent)
        cur.execute("""
                CREATE TABLE IF Not Exists `library_db`.`persons` (
                `id` int NOT NULL AUTO_INCREMENT,
                `personal_code` varchar(45) DEFAULT NULL,
                `name` varchar(45) NOT NULL,
                `last_name` varchar(45) NOT NULL,
                `dob` varchar(45) NOT NULL,
                `added_user_id` varchar(45) DEFAULT NULL,
                `ts_added` datetime DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE KEY `id_UNIQUE` (`id`) /*!80000 INVISIBLE */,
                UNIQUE KEY `personal_code_UNIQUE` (`personal_code`)
                )
                """
            )
        
        # create READERS table (child)
        cur.execute("""
                CREATE TABLE IF Not Exists `library_db`.`readers` (
                `id` varchar(45) NOT NULL,
                `person_id` int NOT NULL,
                `client_card_no` varchar(45) NOT NULL,
                `status` int NOT NULL,
                `added_user_id` varchar(45) DEFAULT NULL,
                `ts_added` datetime DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE KEY `id_UNIQUE` (`id`) /*!80000 INVISIBLE */,
                FOREIGN KEY (`person_id`) REFERENCES `persons` (`id`)
                )
                """
            )
        
        # add entry to PERSONS table
        cur.execute("""
            INSERT INTO persons (personal_code, name, last_name, dob, added_user_id)
            VALUES (%s, %s, %s, %s, %s)
            """, (self.personal_code, self.name, self.last_name, self.dob, self.added_user_id)
        )
        conn.commit()
        
        # Get the auto-incremented ID
        person_id = cur.lastrowid
        
        # add entry to READERS table    
        cur.execute("""
            INSERT INTO readers (id, person_id, client_card_no, status, added_user_id)
            VALUES (%s, %s, %s, %s, %s)
            """, (self.id, person_id, self.client_card_no, self.status, self.added_user_id)
        )
        conn.commit()
        
        conn.close()