from selenium import webdriver
import os
import web_scrapper.constants as const
from time import sleep
import pandas as pd
import json

class MeliScrapper(webdriver.Edge):
    def __init__(self, driver_path=r"C:/Users/nicol/Downloads/edgedriver_win64", 
                teardown=False):
        # the initialization method
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        options = webdriver.EdgeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(MeliScrapper, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
        

    def __exit__(self, exc_type, exc_val, exc_tb):
        # in case I want to close I set teardown as True in the excecution method
        if self.teardown:
            self.quit()
        print("end of the execution")


    def land_first_page(self):
        # we access the landing page
        self.get(const.BASE_URL)

    def filter_by_category(self):
        # filterts by a specific category
        list_elements = self.find_elements_by_class_name("list_element")

        for element in list_elements:
            if "Deportes y Fitness" in element.get_attribute("innerText"):
                
                link = element.get_property("href")
                self.get(link)
                break

    def check_category_from_config(self):
        pass
    
    def get_deals_links(self):
        deals_list = self.find_elements_by_class_name("promotion-item")
        current_url = self.current_url
        links_list = []
        # deals_list[1].click()
        for deal in deals_list:
            deal_link = deal.find_element_by_tag_name("a").get_property("href")
            links_list.append(deal_link)

        print("copy links")

        return links_list, current_url
            

    def open_deal_links(self, links_list):
        deals_details = []
        counter = 0
        sleep(2)

        for link in links_list:
            sleep(2)
            print("open link")
            self.get(link)
            self.implicitly_wait(15)
            sleep(2)
            deal_attributes = self.copy_deal_attributes()
            self.implicitly_wait(15)
            deals_details.append(deal_attributes)
            sleep(2)
            # print(deals_details)

            # this is only for making testing shorter. We are not copying all the data
            counter += 1
            if counter == 8:
                break
        

        return deals_details

    def parse_price_as_int(self, price_str:str):
        """This method takes a price element extracted from the website as a string and returns it as an integer"""
        splitted_price = price_str.split(".")
        joined_price_as_str = ""
        for element in splitted_price:
            joined_price_as_str = joined_price_as_str + element

        price_as_int = int(joined_price_as_str)
        return price_as_int


    def copy_deal_attributes(self):
        attributes_list = []
        
        try:
            title = self.find_element_by_css_selector('h1[class="ui-pdp-title"]').get_attribute("innerText").strip()
        except:
            title = "NaN"
        # sleep(1)
        
        try:
            price = self.parse_price_as_int(
                self.find_element_by_css_selector('div[class="ui-pdp-price__second-line"]').find_element_by_css_selector(
                'span[class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"]').find_element_by_css_selector(
                    'span[class="andes-money-amount__fraction"]'
                ).get_attribute("innerText").strip()
            )
        except:
            price = None
        # sleep(1)

        try:
            deal_image_url = self.find_element_by_css_selector('img[data-index="0"]').get_property("src")
        except:
            deal_image_url = "NaN"
        # sleep(1)

        try:
            seller_recent_sales = int(
                self.find_element_by_css_selector(
                'div[class="ui-pdp-seller__reputation-info"]'). find_element_by_css_selector(
                    'strong[class="ui-pdp-seller__sales-description"]'
                ).get_attribute("innerText").strip()
                )
        except:
            seller_recent_sales = "NaN"
        # sleep(1)

        


        product_description = self.find_element_by_css_selector('p[class="ui-pdp-description__content"]').get_attribute("innerText")
        # sleep(2)
        try:
            product_rating = self.find_element_by_css_selector('p[class="ui-review-view__rating__summary__average"]').get_attribute("innerText").strip()
        except:
            product_rating = "NaN"
        # sleep(2)
        # try:

        #     seller_location = self.find_element_by_css_selector('p[class="ui-seller-info__status-info__subtitle"]').get_attribute("innerText").strip()
        #     if seller_location == "¡Es uno de los mejores del sitio!":
        #         seller_location = "NaN"
        # except:
            
        seller_location = "NaN"
        try:
            seller_rating = self.find_element_by_css_selector('p[class="ui-seller-info__status-info__title ui-pdp-seller__status-title"]').get_attribute("innerText").strip()
        except:
            seller_rating = "NaN"
        try:
            product_category = self.find_elements_by_class_name("andes-breadcrumb__item")[-1].find_element_by_tag_name("a").get_attribute("innerText").strip()
        except:
            product_category = "NaN"

        sleep(2)
        # print(title, price, deal_image_url, seller_recent_sales, product_description, product_rating, seller_location, seller_rating)
        attributes_list = [title, price, deal_image_url, seller_recent_sales, product_description, product_rating, seller_location, seller_rating, product_category]
        # print(attributes_list)
        return attributes_list
        
    def check_last_page_from_previous_session(self):
        with open(os.path.join(os.path.dirname(__file__), "bot_config.json"), "r") as r_file:
            configuration_data = json.load(r_file)
            last_page = configuration_data["last_page"]
        # config_file = open(os.path.join(os.path.dirname(__file__), "bot_config.json"))

        # configuration_data = json.load(config_file)
        
        return last_page

    def save_last_page(self, last_page_param):
        with open(os.path.join(os.path.dirname(__file__), "bot_config.json"), "r") as r_file:
            configuration_data = json.load(r_file)
            configuration_data["last_page"] = last_page_param
            # configuration_data_dict = dict(configuration_data)
            # type(configuration_data_dict)
            with open(os.path.join(os.path.dirname(__file__), "bot_config.json"), "w") as w_file:
                json.dump(configuration_data, w_file)
        # config_file = open(os.path.join(os.path.dirname(__file__), "bot_config.json"))
        # configuration_data = json.load(config_file)
        # configuration_data["last_page"] = last_page



    def go_to_last_page_from_previous_session(self, last_page_number):
        # current_page = 
        return 0

    def write_to_csv(self, deals_dataframe):
        deals_dataframe.to_csv(os.path.join(os.path.dirname(__file__), "deals.csv"))

    def read_from_csv(self):
        deals_data = pd.read_csv('titanic.csv')
        
        return deals_data

    def click_next_page(self, current_search_url):
        self.get(current_search_url)
        self.implicitly_wait(15)
        sleep(4)

        try:
            next_page_button = self.find_element_by_css_selector('li[class="andes-pagination__button andes-pagination__button--next"]').find_element_by_tag_name("a")
            next_page_link = next_page_button.get_property("href")
            self.get(next_page_link)
            self.implicitly_wait(15)
            sleep(3)
            return False

        except:
            print("There are no more pages")
            return True
