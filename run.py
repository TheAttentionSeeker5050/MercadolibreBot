"""

    the structure of the program should be:
    1. access the filtered views, go to a last from the csv file page if the process was interrupted
    2. open one of the items link
    3. copy all the attributes on a list
    4. save the last page in a text file. To go back in case it is interrupted
    5. repeat the steps 2,3,4 until we run out of items in a page
    4. generate dataframe from all the deals in a specific page
    5. append the dataframe to the global dataframe, save dataframe to a csv file when done or the process is interrupted
    6. go to the next page when it is done
    7. repeat steps 2-6 until there are no next pages.

"""

from time import sleep
from web_scrapper.scrapper import MeliScrapper
import pandas as pd

col_names = ["Product title", "Price", "Deal image url", "Recent sales", "Description", "Product rating", "Seller location", "Seller Rating", "Product category"]
all_deals_dataframe = pd.DataFrame(columns=col_names)

with MeliScrapper() as bot:
    bot.land_first_page()
    sleep(2)
    bot.filter_by_category()
    sleep(3)
    
    last_page = bot.check_last_page_from_previous_session()
    print(last_page)
    no_more_pages = False
    
    
    while no_more_pages == False:
        links_list, current_search_page_url = bot.get_deals_links()
        sleep(2)
        all_items_in_page = bot.open_deal_links(links_list)
        sleep(2)
        page_dataframe = pd.DataFrame(all_items_in_page ,columns=col_names)
        all_deals_dataframe = all_deals_dataframe.append(page_dataframe)
        print(all_deals_dataframe)
        bot.write_to_csv(all_deals_dataframe)
        sleep(2)
        last_page += 1
        bot.save_last_page(last_page)
        no_more_pages = bot.click_next_page(current_search_page_url)
        sleep(3)

    print("End of the execution")




