from create_trello_cards.providers import Provider
from create_trello_cards.utility import get_soup

class Udemy(Provider):
    """Class to get all the courses from udemy"""
    
    def __init__(self, user_id):
        """Constructor to the Udemy class"""
        self.user_id = user_id
        self.url = "https://www.udemy.com/user/{}/".format(self.user_id)
        self.soup = get_soup(self.url)
        self.courses = []
        self.get_cards()

    def get_cards(self):
        self.get_all_pages()
        return self.courses

    def get_titles(self, soup):
        """Get all course titles from a page"""
        titles = []
        for course in soup.find_all('li', {'class':'card'}):
            title = course.find('strong', {'class':'details__name'}).text.strip().strip('\n').strip()
            url = course.find('a').get('href')
            img = course.find('img', {'class': 'img'}).get('src')
            titles.append({'title': title, 'url': 'https://www.udemy.com{}'.format(url), 'thumbnail': img})
        return titles

    def get_all_pages(self):
        """Methog to get all the pages from udemy course"""
        pages = self.get_max_pages()
        for i in range(1, int(pages)+1):
            url = "https://udemy.com/user/{}/?subscribed_courses={}&key=subscribed_courses".format(self.get_user_id(), i)
            soup = get_soup(url)
            self.courses.extend(self.get_titles(soup))

    def get_user_id(self):
        """Method to get the user id from the url"""
        return self.url.strip('/').split('/')[-1]

    def get_max_pages(self):
        pages_text = self.soup.find('ul', {'class':'pagination'}).find_all('li')[-2].text
        return pages_text.strip().strip('\n').strip()

    def get_curriculum(self, url):
        """
        Get the currliculum from any udemy course url
        """
        soup = get_soup(url)
        c = soup.find('div', {'class':'curriculum-wrapper'})
        return [ x.text for x in c.find_all('span', {'class':'lecture-title-text'}) ]
