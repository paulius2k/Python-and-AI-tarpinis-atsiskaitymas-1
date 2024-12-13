import time
from datetime import datetime

class Transaction:
    """
    A transaction between the library and the client-reader (e.g. lending, returning am item)
    """
    
    def __init__(self, client_id:str, item_id:str, amount:int, txn_type:int, txn_status:int, start_dt:datetime, finish_dt:datetime, ts_modified: datetime, comment:str = "", added_user_id:str = "u-999") -> None:
        self.client_id:str = client_id
        self.item_id:str = item_id
        self.amount:int = amount                    # amount of items
        self.txn_type:int = txn_type                # 1-lend, 2-return
        self.txn_status:int = txn_status            # 1-open, 2-closed
        self.start_dt:datetime = start_dt           # e.g. lending period start date
        self.finish_dt:datetime = finish_dt         # e.g. lending period deadline date
        self.comment: str = comment                 # free text comment
        self._added_user_id:str = added_user_id
        self._ts_modified:datetime = ts_modified

        self._id:str = f"t-{str(int(time.time() * 100))}"     # t - transaction
        self._ts_added:datetime = datetime.today()

    def __str__(self):
        return (
            f"[{self._id}, "
            f"{self.client_id}, "
            f"{self.item_id}, "
            f"{self.amount}, "
            f"{self.txn_type}, "
            f"{self.txn_status}, "
            f"{self.start_dt}, "
            f"{self.finish_dt}, "
            f"{self._added_user_id}]"
        )
    
    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{self._id}, "
            f"{self.client_id}, "
            f"{self.item_id}, "
            f"{self.amount}, "
            f"{self.txn_type}, "
            f"{self.txn_status}, "
            f"{self.start_dt}, "
            f"{self.finish_dt}, "
            f"{self._added_user_id})"
        )
    
    