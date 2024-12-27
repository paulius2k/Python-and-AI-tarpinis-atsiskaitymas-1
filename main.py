from views.menus import main_menu_logic
from classes.catalogue import Catalogue
from classes.clients import Clients
from classes.registry import Registry
import sys

if __name__ == '__main__':
    
    try:
        new_catalogue = Catalogue()
        new_clients_db = Clients()
        new_registry = Registry()
        
        # mark all overdue transactions
        new_registry.mark_overdue_transactions()
        
        # call main manu loop
        main_menu_logic(new_catalogue, new_clients_db, new_registry)
    except Exception as err:
        print(f"Error: {err}")
        sys.exit(1)
        
 