from selenium import webdriver
import config
import re
import pandas as pd
from movie_details import Movie


class IMDBTop250Page:
    def __init__(self):
        self.url = config.url
        self.driver = webdriver.Chrome(
            executable_path=config.chrome_driver_path,
            options=config.option)
        self.driver.get(self.url)
        self.movie_table_xpath = '//*[@id="main"]/div/span/div/div/div[3]/table/tbody'
        self.movie_table_element = self.__set_movie_table_element()
        self.movie_row_elements = self.__set_movie_row_elements()
        self.movie_dataframe = self.__set_movie_dataframe_and_objects()[0]
        self.movie_objects = self.__set_movie_dataframe_and_objects()[1]
        self.driver.quit()

    def __set_movie_table_element(self):
        return self.driver.find_element_by_xpath(self.movie_table_xpath)

    def __set_movie_row_elements(self):
        return self.movie_table_element.find_elements_by_tag_name('tr')

    def __set_movie_dataframe_and_objects(self):
        df_row_list = []
        movie_object_list = []
        id = 1
        for row_element in self.movie_row_elements:
            title_td = row_element.find_element_by_class_name('titleColumn')
            rating_td = row_element.find_elements_by_tag_name('td')[2]
            movie_title = title_td.find_element_by_tag_name('a').text
            movie_year = re.sub(r'[\)\(]', '', title_td.find_element_by_css_selector('.secondaryInfo').text)
            movie_page_link = title_td.find_element_by_tag_name('a').get_attribute('href')
            rating = rating_td.text
            df_row_list.append([id, movie_title, movie_year, rating, movie_page_link])
            movie = Movie(id=id, name=movie_title, link=movie_page_link)
            movie_object_list.append(movie)
            id = id + 1
        data = df_row_list
        columns = ['id', 'movie_title', 'movie_year', 'rating', 'movie_page_link']
        df_movie = pd.DataFrame(data, columns=columns)
        return df_movie, movie_object_list


if __name__ == '__main__':
    top_250_object = IMDBTop250Page()
    print('x')
