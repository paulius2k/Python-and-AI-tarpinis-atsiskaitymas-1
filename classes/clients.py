from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
import pickle
import os
from datetime import datetime
import constants as const
from classes.reader import Reader

class Clients:
    """
    A list of all library clients-readers
    """
    def __init__(self):
        # First try to load data from file if such exists
        if os.path.isfile(const.CLIENTS_FILE_NAME):
            with open(const.CLIENTS_FILE_NAME, "rb") as file:
                obj = pickle.load(file)

            # copy all attributes from the loaded object to self
            self.__dict__.update(obj.__dict__)
            
        else:
            self.items = []
        
    def __str__(self):
        result = ""
        for item in self.items:
            result += f"{item}\n"
        return result
       
    def _dump_data_to_storage(self):
        result = 0
        msg = ""
        
        try:
            with open(const.CLIENTS_FILE_NAME, "wb") as file:
                pickle.dump(self, file)
            result = 1
            msg = f"Data stored successfully"
            
        except Exception as err:
            msg = f"Error storing data. {err}\n"
        
        return (result, msg)
       
    def add_client(self):
        """Add new Reader to the catalogue"""
    
        # inner funtion to validate date-of-birth
        def input_datetime_validator(value):
            try:
                datetime_format = "%Y-%m-%d"  
                datetime.strptime(value, datetime_format)
                return True  # Input is valid
            except Exception:
                return False # Input invalid
    
        result = ()        
        
        try:       
            # inform user that new client database will be created because there was none found / or it was empty
            if not self.items:
                print("Creating a new client database.\n")

            # form a list of input fields to user (using InquirerPy library)
            
            status_options = {
                1: "active",
                2: "not active",
            }
            status_choices = [{"name": value, "value": key} for key, value in status_options.items()]
            
            
            questions = [
                {
                    "type": "input", 
                    "message": "Enter client name:",
                    "validate": EmptyInputValidator(),
                    "name": "name",
                },
                {
                    "type": "input", 
                    "message": "Enter client last name:", 
                    "validate": EmptyInputValidator(),
                    "name": "last_name",
                },
                {
                    "type": "input", 
                    "message": "Enter client date of birth (YYYY-MM-DD):", 
                    "validate": input_datetime_validator,
                    "invalid_message": "Input should be in date format YYYY-MM-DD.",
                    "name": "dob"
                },
                {
                    "type": "input", 
                    "message": "Enter client card number:", 
                    "validate": EmptyInputValidator(),
                    "name": "client_card_no",
                },
                {
                    "type": "rawlist", 
                    "message": "Select client status:", 
                    "choices": status_choices,
                    "name": "status", 
                },

            ]
            
            # show a list of input fields to user and ask for data input
            answers = prompt(
                questions,
                keybindings={"interrupt": [{"key": "escape"}]},
                # raise_keyboard_interrupt=False
                )

            if answers:
                
                datetime_format = "%Y-%m-%d"  
                dob_dt = datetime.strptime(answers["dob"], datetime_format)
                
                new_item = Reader(
                    name = answers["name"],
                    last_name = answers["last_name"],
                    dob = dob_dt,
                    client_card_no = answers["client_card_no"],
                    status = int(answers["status"])
                )
                
                self.items.append(new_item)
                
            # save data to file
            result = self._dump_data_to_storage()
                
        except KeyboardInterrupt as err:
            result = (0, f"Entry cancelled by user. Client was not saved to the database.\n")        
        except Exception as err:
            result = (0, f"{err}\n")
        
        return result

    def get_clients(self, search_phrase = "", item_status = 1):
        """Returns a list of clients from the database by search criteria"""

        found_clients = []    
        
        if self.items:                
            for item in self.items:
                if item.status == item_status:
                    if search_phrase:
                        if search_phrase.lower() in item.__str__().lower() and item.status == item_status:
                            found_clients.append(item)    
                    else:
                        found_clients.append(item)     

        return found_clients
                
    
    def deactivate_client(self, id):
        """Marks a client as non-active"""
        
        result = ()
        
        try:
            for item in self.items:
                if item.id == id:
                    item.status = 2
                    dump_result = self._dump_data_to_storage()
                    result = (1, "\nItem deleted successfully")
                    break
        
        except Exception as err:
            result = (0, f"Error disactivating client: {err}\n")
        
        return result
    
    