from InquirerPy import prompt
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.validator import Validator
from functools import partial
from datetime import datetime, timedelta
import pickle
import os
import constants as const
from classes.transaction import Transaction
from classes.catalogue import Catalogue

class Registry:
    """
    A registry of transactions between the library and the readers
    """
    def __init__(self):
        # First try to load data from file if such exists
        if os.path.isfile(const.REGISTRY_FILE_NAME):
            with open(const.REGISTRY_FILE_NAME, "rb") as file:
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
            with open(const.REGISTRY_FILE_NAME, "wb") as file:
                pickle.dump(self, file)
            result = 1
            msg = f"Data stored successfully"
            
        except Exception as err:
            msg = f"Error storing data. {err}\n"
        
        return (result, msg)          

    def new_transaction(self, items_catalogue: Catalogue, client_id, item_id, max_amount, txn_type, start_dt):
        """Register new transaction between the library and the client"""
        
        # custom date input validator for InquirerPy selection
        def datetime_validator(value_str, min:datetime, max:datetime):
            try:
                # Define your expected datetime format
                datetime_format = "%Y-%m-%d"  
                value_dt = datetime.strptime(value_str, datetime_format)
                min = min.replace(hour=0, minute=0, second=0, microsecond=0)
                max = max.replace(hour=0, minute=0, second=0, microsecond=0)
                
                if min <= value_dt <= max:
                    return True  # Input is valid
                
            except Exception:
                return False

        result = ()
        
        try:       
            # inform user that new catalogue will be created because there was none found / or it was empty
            if not self.items:
                print("Creating new registry.\n")


            if int(txn_type) == 1:      # lend
                txn_status = 1          # open
                min_amount = 1
                default_amount = None
                default_start_dt = start_dt.strftime("%Y-%m-%d")
            elif int(txn_type) == 2:    # return
                txn_status = 2          # closed                      
                min_amount = max_amount
                default_amount = max_amount    
            
            from_date_validator_with_params = Validator.from_callable(
                partial(datetime_validator, min=datetime.today(), max=datetime.today() + timedelta(days=30))
                )   
            
            
            # form a list of input fields to user (using InquirerPy library)
            questions = [
                {
                    "type": "number", 
                    "message": "Number of items:", 
                    "min_allowed": min_amount,
                    "max_allowed": max_amount,
                    "default": default_amount,
                    "validate": EmptyInputValidator(),
                    "invalid_message": "Input should be number.",
                    "name": "amount"
                },
                {
                    "type": "input", 
                    "message": "Starting date (YYYY-MM-DD):",
                    "default": default_start_dt,                    
                    "validate": from_date_validator_with_params,
                    "invalid_message": "format YYYY-MM-DD, min today.",
                    "name": "start_dt"
                },
                {
                    "type": "input", 
                    "message": "Deadline date (YYYY-MM-DD):", 
                    "validate": from_date_validator_with_params,
                    "invalid_message": "format YYYY-MM-DD.",
                    "name": "finish_dt"
                },
                {
                    "type": "input", 
                    "message": "Comment (optional):",
                    "name": "comment",
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
                start_dt_dt = datetime.strptime(answers["start_dt"], datetime_format)
                finish_dt_dt = datetime.strptime(answers["finish_dt"], datetime_format)
                
                if int(txn_type) == 1:      # lend
                    change_amount = int(answers["amount"]) * (-1)
                elif int(txn_type) == 2:    # return
                    change_amount = int(answers["amount"])      
                                    
                new_item = Transaction(
                    client_id = client_id,
                    item_id = item_id,
                    amount = int(answers["amount"]),
                    txn_type = int(txn_type),
                    txn_status = txn_status,
                    start_dt = start_dt_dt,
                    finish_dt = finish_dt_dt,
                    comment = answers["comment"],
                    ts_modified = datetime.today()
                )
                
                self.items.append(new_item)               
                # save data to file
                result = self._dump_data_to_storage()
                
                # UPDATE item balance in the catalogue
                items_catalogue.update_item_balance(item_id, change_amount)
                
                
        except KeyboardInterrupt as err:
            result = (0, f"Entry cancelled by user. Transaction was not saved.\n")        
        except Exception as err:
            result = (0, f"{err}\n")
        
        return result

    def get_transactions(self, search_phrase = "", txn_status = 1):
        """Returns a list of transactions from the registry based on request criteria"""

        found_items = []    
        
        if txn_status == 0:
            status_list = {1,2}
        else:
            status_list = {txn_status}
        
        if self.items:                
            for item in self.items:
                if item.txn_status in status_list:
                    if search_phrase:
                        if search_phrase.lower() in item.__str__().lower():
                            found_items.append(item)    
                    else:
                        found_items.append(item)     
        
        return found_items
    


