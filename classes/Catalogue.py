from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from datetime import datetime
from classes.item import Item
from modules.utilities import Database

class Catalogue:
    """
    A catalogue of all items the library owns.
    """
    def __init__(self):
        conn = Database.get_connection()
        cur = conn.cursor()
        
        # Fetch all items
        cur.execute('''
                    SELECT id, title, author, publication_year, genre, type, total_units, available_units, status, added_user_id
                    FROM library_db.items
                ''')
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if rows:
            self.items = [Item(                    
                    id=row[0],
                    title=row[1], 
                    author=row[2], 
                    publication_year=row[3], 
                    genre=row[4],
                    type=row[5],
                    total_units=row[6],
                    available_units=row[7],
                    status=row[8],
                    added_user_id=row[9]
                    )
                for row in rows]
        else:
            self.items = []     
        
    def __str__(self):
        result = ""
        for item in self.items:
            result += f"{item}\n"
        return result
       
    # def _dump_data_to_storage(self):
    #     result = 0
    #     msg = ""
        
    #     try:
    #         with open(const.CATALOGUE_FILE_NAME, "wb") as file:
    #             pickle.dump(self, file)
    #         result = 1
    #         msg = f"Data stored successfully"
            
    #     except Exception as err:
    #         msg = f"Error storing data. {err}\n"
        
    #     return (result, msg)
    
    def add_book(self):
        """Add new Book to the catalogue"""
        
        result = ()
        
        try:       
            # inform user that new catalogue will be created because there was none found / or it was empty
            if not self.items:
                print("Creating new catalogue.\n")

            # form a list of input fields to user (using InquirerPy library)
            questions = [
                {
                    "type": "input", 
                    "message": "Enter the book title:",
                    "validate": EmptyInputValidator(),
                    "name": "title",
                },
                {
                    "type": "input", 
                    "message": "Enter the author:",
                    "validate": EmptyInputValidator(),                    
                    "name": "author",
                },
                {
                    "type": "number", 
                    "message": "Enter year of publication:", 
                    "min_allowed": 1,
                    "max_allowed": datetime.today().year + 1,
                    "default": None,
                    "validate": EmptyInputValidator(),
                    "invalid_message": "Input should be number.",
                    "name": "publication_year"
                },
                {
                    "type": "rawlist", 
                    "message": "Select genre:", 
                    "choices": ["Fiction", "Non-Fiction", "Science Fiction (Sci-Fi)","Mystery/Thriller","Romance", "Horror", "Historical Fiction", "Young Adult (YA)","Poetry"],
                    "name": "genre", 
                },
                {
                    "type": "number", 
                    "message": "How many units received:", 
                    "min_allowed": 1,
                    "max_allowed": 100,
                    "validate": EmptyInputValidator(),
                    "default": None,
                    "invalid_message": "Input should be number.",
                    "name": "total_units"
                },
            ]
            
            # show a list of input fields to user and ask for data input
            answers = prompt(
                questions,
                keybindings={"interrupt": [{"key": "escape"}]},
                # raise_keyboard_interrupt=False
                )

            if answers:
                new_item = Item(
                    title = answers["title"],
                    author = answers["author"],
                    publication_year = int(answers["publication_year"]),
                    type = 1,   # 1 - book, 2 - magazine
                    genre = answers["genre"],
                    total_units = int(answers["total_units"]),
                    available_units = int(answers["total_units"])
                )               
                
                new_item.save()
                
                self.__init__()
                
                result = 1 
                msg = f"\nItem added successfully"
                
                
                
            # save data to file
            # result = self._dump_data_to_storage()
                
        except KeyboardInterrupt as err:
            result = 0
            msg = f"Entry cancelled by user. Item was not saved.\n"        
        except Exception as err:
            result = 0
            msg = f"{err}\n"
        
        return (result, msg)

    def get_items(self, search_phrase = "", item_status = 1):
        """Returns a list of items from the catalogue depending of request criteria"""

        found_items = []    
        
        if self.items:                
            for item in self.items:
                if item.status == item_status:
                    if search_phrase:
                        if search_phrase.lower() in item.__str__().lower() and item.status == item_status:
                            found_items.append(item)    
                    else:
                        found_items.append(item)     
        
        return found_items
    
    def get_item_by_id(self, id):
        """Returns a item by its id"""
        
        if self.items:                
            for item in self.items:
                if item.id == id:
                    found_item = item     
                    break
        return found_item
    
    def delete_item(self, id:str):
        """Marks item as deleted"""
        
        result = ()
        
        try:
            for item in self.items:
                if item.id == id:
                    # update item status to 2 (deleted)
                    # item.status = 2
                    # dump_result = self._dump_data_to_storage()
                    
                    conn = Database.get_connection()
                    cur = conn.cursor()
    
                    cur.execute('''
                                UPDATE library_db.items
                                SET
                                status = 2
                                WHERE id = %s;
                            ''', (id,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    
                    self.__init__()                   
                    
                    result = (1, "\nItem deleted successfully")
                    break
        
        except Exception as err:
            result = (0, f"Error deleting item: {err}\n")
        
        return result
    
    def update_item_balance(self, id:str, change_amount: int):
        """Updates available units of the item after lend/return transaction"""
        
        result = ()
        
        try:
            for item in self.items:
                if item.id == id:
                    new_amount = item.available_units + change_amount
                     
                    if new_amount < 0 or item.available_units < 0:
                        result = (0, "\nThere are no available units of this item in the library.")
                        break    
                    elif new_amount > item.total_units:
                        result = (0, "\nAmount of available units after the transaction would exceed the total units owned by the library. Transaction not possible.")
                        break
                    else:                        
                        # update record in the database
                        ## item.available_units = new_amount
                        ## dump_result = self._dump_data_to_storage()

                        conn = Database.get_connection()
                        cur = conn.cursor()
        
                        cur.execute('''
                                    UPDATE library_db.items
                                    SET
                                    available_units = %s
                                    WHERE id = %s;
                                ''', (new_amount, id))
                        conn.commit()
                        cur.close()
                        conn.close()
                        
                        self.__init__()
                             
                        result = (1, "\nItem updated successfully")
                        break
                else:
                    result = (0, "\nSuch item not found in the catalogue.")
        except Exception as err:
            result = (0, f"Error updating item: {err}\n")
        
        return result 
    
