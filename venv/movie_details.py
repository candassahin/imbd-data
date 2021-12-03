class Movie:

    def __init__(self, id, name, link, driver):
        self.id = id
        self.name = name
        self.link = link
        self.driver = driver
        driver.get(self.link)
        self.movie_details = self.__set_movie_details()

    def __set_movie_details(self):
        pass