from views.menus import main_menu_logic
import modules.tx_actions as tx_actions
from classes.catalogue import Catalogue
from classes.clients import Clients
from classes.registry import Registry

if __name__ == '__main__':
    new_catalogue = Catalogue()
    new_clients_db = Clients()
    new_registry = Registry()
    
    # mark all overdue transactions
    new_registry.mark_overdue_transactions()
    
    # call main manu loop
    main_menu_logic(new_catalogue, new_clients_db, new_registry)
        
 