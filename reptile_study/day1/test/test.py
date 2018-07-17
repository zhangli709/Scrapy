from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup


def get_title(url):
    try:
        html = urlopen(url)
    except (HTTPError, URLError) as e:
        return None
    try:
        bs_obj = BeautifulSoup(html.read())
        title = bs_obj.body.h1
    except AttributeError as e:
        return None
    return title


title = get_title('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print("Title could not be found")
else:
    print(title)