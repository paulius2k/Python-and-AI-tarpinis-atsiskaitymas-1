from views.menus import main_menu_logic
from classes.catalogue import Catalogue
from classes.clients import Clients

if __name__ == '__main__':
    new_catalogue = Catalogue()
    new_clients_db = Clients()
    
    main_menu_logic(new_catalogue, new_clients_db)
    
 