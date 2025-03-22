## Importing important libraries
import time
import selenium

import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ReviewScrapper:
    
    def __init__(self,driver,timeout = 5):
        
        self.driver = driver
        self.wait = WebDriverWait(self.driver,timeout=timeout)
        
    def wait_for_page_to_load(self):
        
        try:
            
            self.wait.until(lambda d:d.execute_script("return document.readyState")=='complete')
            
        except:
            
            print(f'timeout page {self.driver.title} is not loaded in given duration')
            
        else:
            
            print(f'page {self.driver.title} is loaded in given duration')
            

    def access_movie(self,movie_name:str):
        ## locate search bar and enter movie name
        search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="suggestion-search"]')))
        search_box.send_keys(movie_name)

        ## locate search button and click the search button
        search_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="suggestion-search-button"]')))
        search_button.click()

        ## select movie from list of movies
        moview = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]/div/a'))).click()
        time.sleep(1)

        ## select user review button and click on it
        self.wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='User reviews']"))).click()

        ## remove reviews which have spoilers
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="title-reviews-hide-spoilers"]'))).click()

    def navigate_to_review_page(self):

        ## scroll at the bottom of page and load all the reviews
        while True:
            
            try:
                
                time.sleep(2)
                all_reviews = self.driver.find_element(By.XPATH,"//span[@class='ipc-see-more__text'][normalize-space()='All']")
                
            except:
                
                print(f'timeout button is not available')
                ann = self.driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/section/div/section/div/div[1]/section[2]/div[1]/hgroup/h3/span')
                self.driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - 100);", ann)
                break
                
            else:
                
                self.driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - 100);", all_reviews)
                time.sleep(5)
                
                self.wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='ipc-see-more__text'][normalize-space()='All']"))).click()
                time.sleep(20)

    def scrap_reviews(self):
        
        rows = self.driver.find_elements(By.CLASS_NAME,'ipc-list-card__content')
        
        rating = []
        review_title = []
        review_text = []
        
        for row in rows:
            try:
                star_rating = row.find_element(By.CLASS_NAME,'ipc-rating-star--rating').text.strip()
            except:
                star_rating = np.nan
            title = row.find_element(By.CLASS_NAME,'ipc-title__text').text
            text = row.find_element(By.CLASS_NAME,'ipc-html-content-inner-div').text
        
            rating.append(float(star_rating))
            review_text.append(text)
            review_title.append(text)

        self.df = pd.DataFrame({'Rating':rating,'Title':review_title,'Review_text':review_text})
        
    def clean_dataframe(self,filename):
        self.df['Sentiment'] = self.df.apply(lambda row:1 if row['Rating']>5 else 0,axis = 1)
        self.df.drop_duplicates(inplace = True)

        self.df.to_csv(filename + '.csv', index = False)


if __name__ == "__main__":

    driver = webdriver.Chrome()
    driver.maximize_window()
    url = 'https://www.imdb.com'
    driver.get(url)
    review = ReviewScrapper(driver,5)
    review.access_movie('Adipurush')
    review.navigate_to_review_page()
    review.scrap_reviews()
    review.clean_dataframe('adipurush_reviews')