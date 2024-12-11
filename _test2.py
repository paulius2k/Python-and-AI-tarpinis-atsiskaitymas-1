from classes.book import Book
import modules.services as services
import constants as const


catalogue = []
load_result = services.load_data_from_storage(const.CATALOGUE_FILE_NAME)
catalogue = load_result[0]

for item in catalogue:
    print(f"Status prieš: {item.status}")
    # item.status = 1
    print(f"Status po: {item.status}")
    print(item.__repr__())

# services.dump_data_to_storage(const.CATALOGUE_FILE_NAME, catalogue)

    

