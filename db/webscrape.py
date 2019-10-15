from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
import re

REMOVE_COLS = ['scrape_id','last_scraped','smart_location','calendar_last_scraped']

HOST_COLS = ['host_id','host_url','host_name','host_since',
'host_location','host_about','host_response_time','host_response_rate',
'host_acceptance_rate','host_is_superhost','host_thumbnail_url',
'host_picture_url','host_neighbourhood','host_listings_count',
'host_total_listings_count','host_verifications',
'host_has_profile_pic','host_identity_verified']

driver = Chrome('/Users/ridleyleisy/Downloads/chromedriver 2')
driver.get('http://insideairbnb.com/get-the-data.html')
tables = driver.find_elements_by_tag_name('table')

us_list = []
unique_cities = []
flat_list = []

for table in tables:
    sub_table = table.find_elements_by_css_selector('a')
    for sub in sub_table:
        url = sub.get_attribute('href')
        print(url)
        if ('united-states' in url) & ('visualisations' not in url):
            us_list.append(url)

breakdown = [re.split('/',x) for x in us_list]

for index, inner in enumerate(breakdown):
    unique_cities.append(inner[5:6])

for sublist in unique_cities:
    for item in sublist:
        flat_list.append(item)
<<<<<<< HEAD
# seed db here


# delete files


print(set(flat_list))
=======
>>>>>>> routes
