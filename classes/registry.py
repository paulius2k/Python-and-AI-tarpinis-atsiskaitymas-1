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

    def new_transaction(self, items_catalogue: Catalogue, client_id, item_id, max_amount, txn_type, start_dt, finish_dt=""):
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
        questions = []
        prefilled_answers = {}
        
        try:       
            # inform user that new catalogue will be created because there was none found / or it was empty
            if not self.items:
                print("Creating new registry.\n")

            # prepare some variables and answers in advance, if we know them
            if start_dt:
                default_start_dt = start_dt.strftime("%Y-%m-%d")
            else:
                default_start_dt = ""
                
            return_dt_dt = ""
            
            if int(txn_type) == 1:      # lend
                txn_status = 1          # open

                # amount
                min_amount = 1               
                default_amount = None
                ask_amount = True
                
                # dates
                ask_start_dt = True
                ask_finish_dt = True                

            elif int(txn_type) == 2:    # return
                txn_status = 2          # closed                 
                
                # amount
                prefilled_answers.update({"amount": max_amount})
                ask_amount = False
                
                # dates                
                prefilled_answers.update({"start_dt": default_start_dt})
                ask_start_dt = False
                
                if finish_dt:
                    default_finish_dt = finish_dt.strftime("%Y-%m-%d")
                else:
                    prefilled_answers.update({"finish_dt": ""})
                    
                ask_finish_dt = False                
                
                return_dt_dt = datetime.today()
                return_dt_dt = return_dt_dt.replace(hour=0, minute=0, second=0, microsecond=0)
                prefilled_answers.update({"return_dt": return_dt_dt})
                                
            from_date_validator_with_params = Validator.from_callable(
                partial(datetime_validator, min=datetime.today(), max=datetime.today() + timedelta(days=30))
                )   
            
            # form a list of input fields to user (using InquirerPy library)
            if ask_amount:
                questions.append(
                    {
                        "type": "number", 
                        "message": "Number of items:", 
                        "min_allowed": min_amount,
                        "max_allowed": max_amount,
                        "default": default_amount,
                        "validate": EmptyInputValidator(),
                        "invalid_message": "Input should be number.",
                        "name": "amount"
                    }                
                )
            
            if ask_start_dt:
                questions.append(
                    {
                        "type": "input", 
                        "message": "Starting date (YYYY-MM-DD):",
                        "default": default_start_dt,                    
                        "validate": from_date_validator_with_params,
                        "invalid_message": "format YYYY-MM-DD, min today.",
                        "name": "start_dt"
                    }
                )
 
            if ask_finish_dt:
                questions.append(                       
                    {
                        "type": "input", 
                        "message": "Deadline date (YYYY-MM-DD):", 
                        "validate": from_date_validator_with_params,
                        "invalid_message": "format YYYY-MM-DD.",
                        "name": "finish_dt"
                    }
                )
            
            questions.append( 
                {
                    "type": "input", 
                    "message": "Comment (optional):",
                    "name": "comment",
                }
            )

            
            # show a list of input fields to user and ask for data input
            answers = prompt(
                questions,
                keybindings={"interrupt": [{"key": "escape"}]},
                # raise_keyboard_interrupt=False
                )
            
            # merge answers from user with pre-filled answers
            answers = {**prefilled_answers, **answers}
            
            if answers:
                
                datetime_format = "%Y-%m-%d"
                
                if answers["start_dt"]:
                    start_dt_dt = datetime.strptime(answers["start_dt"], datetime_format)                    
                else:
                    start_dt_dt = ""
                
                if answers["finish_dt"]:
                    finish_dt_dt = datetime.strptime(answers["finish_dt"], datetime_format)
                else:
                    finish_dt_dt = ""
                
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
                    return_dt = return_dt_dt,
                    comment = answers["comment"],
                    ts_modified = datetime.today()
                )           

                # FIRST: try UPDATING item balance in the catalogue
                balance_update_result = items_catalogue.update_item_balance(item_id, change_amount)
                
                if balance_update_result[0] == 1:
                    # ONLY THEN save the transaction
                    self.items.append(new_item)   
                    result = self._dump_data_to_storage()
                else:                
                    result = balance_update_result
                
                
        except KeyboardInterrupt as err:
            result = (0, f"Entry cancelled by user. Transaction was not saved.\n")        
        except Exception as err:
            result = (0, f"{err}\n")
        
        return result

    def close_transaction(self, id):
        """Close the old transaction between the library and the client"""

        result = ()
        
        try:       
            for item in self.items:
                if item._id == id:
                    item.txn_status = 2
                    today_dt = datetime.today()
                    return_dt = today_dt.replace(hour=0, minute=0, second=0, microsecond=0)
                    item.return_dt = return_dt
                    item._ts_modified = return_dt
                    result = self._dump_data_to_storage()
                    return result
                
                else:
                    result = (0, f"Transaction not found.\n")   
                              
        except KeyboardInterrupt as err:
            result = (0, f"Entry cancelled by user. Transaction was not saved.\n")        
        except Exception as err:
            result = (0, f"{err}\n")
        
        return result

    def overdue_transaction(self, id):
        """Make the transaction "overdue" """

        result = ()
        
        try:       
            for item in self.items:
                if item._id == id:
                    item.txn_status = 3
                    today_dt = datetime.today()
                    today_dt = today_dt.replace(hour=0, minute=0, second=0, microsecond=0)
                    item._ts_modified = today_dt
                    result = self._dump_data_to_storage()
                    return result
                
                else:
                    result = (0, f"Transaction not found.\n")   
                              
        except KeyboardInterrupt as err:
            result = (0, f"Entry cancelled by user. Transaction was not saved.\n")        
        except Exception as err:
            result = (0, f"{err}\n")
        
        return result

    def get_transactions(self, client_id, txn_status_set:set = {1,3}):
        """Returns a list of transactions from the registry based on request criteria"""

        found_items = []    
                
        if self.items:                
            for item in self.items:
                if item.txn_status in txn_status_set:
                    if client_id:
                        if item.client_id == client_id:
                            found_items.append(item)    
                    else:
                        found_items.append(item)    
                        
        return found_items
    
    def get_transaction_by_id(self, id):
        """Returns the transaction by its id"""
        
        if self.items:                
            for item in self.items:
                if item._id == id:
                    found_txn = item

        return found_txn

    def mark_overdue_transactions(self):
        try:
            today_dt = datetime.today()
            today_dt = today_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            
            counter = 0

            for item in self.items:
                if item.txn_status == 1 and item.txn_type == 1:
                    if item.finish_dt < today_dt:
                        item.txn_status = 3
                        counter += 1
            
            if counter > 0:
                result = self._dump_data_to_storage()
            else:
                result = (0, "No overdue records found")
        
        except Exception as err:
            result = (0, "Error processing records")
            
        return result
    