"""
This module contains a demonstration for creating RSS feeds from HTML pages.

* We use `requests` to start an HTTP request;
* Then we use `response.text` to retrieve the HTML text;
* We need another library, `pyquery`, for parsing and querying HTML content.
  There are other popular choices, like `lxml` & `beautifulsoup4`, just
  choose one to your taste.
* Finally we transform the retrieved data to a dictionary,
  with all the necessary fields to create a RSS feed.
"""

import requests
import time
from bs4 import BeautifulSoup
import arrow
from rsserpent.utils import cached

path = "/caa/html"

@cached
async def provider() -> dict:
    """Define an example data provider function, who will provide \
    the data needed by RSSerpent to create a RSS feed."""
    base_url = "https://www.caanet.org.cn/"
    index_url = "https://www.caanet.org.cn/news.mx?"
    # Set Cookies
    session = requests.Session()
    session.get(index_url)

    # Build POST
    datas = {
      "pageNo": "3",
      "Ajax": "Ajax",
      "id": "3"
    }
    # init List
    title_list = []
    url_list = []
    date_list = []
    text_list = []
    for i in range(1,4):
        datas["pageNo"] = i
        index_response = session.post(index_url, data=datas)
        soup = BeautifulSoup(index_response.text, "html.parser").select("li a")
        date = BeautifulSoup(index_response.text, "html.parser").select("li span")

        for g in range(len(soup)):
            title_list.append( soup[g].string )
            url = 'https://www.caanet.org.cn/' + soup[g].attrs['href']
            url_list.append(url)
            pub_date = str(date[g]).replace('年', '-').replace('月', '-').replace('日', '').replace('<span>', '').replace('</span>', '')
            date_list.append(pub_date)
            text_response = session.get(url)
            text = BeautifulSoup(text_response.text, "html.parser").select('.page_r')
            text[0].h3.extract()
            text[0].h4.extract()
            for tag in text[0].findAll(True):
                tag.attrs = None
            text_list.append(text[0])
    # returns a dictionary compatible with `rsserpent.model.Feed`
    return {
        "title": "中国美术家协会",
        "link": "https://www.caanet.org.cn/news.mx?id=3",
        "description": "中国美术家协会展览公告通知",
        "items": [
            {
                "title": title_list[r],
                "description": text_list[r],
                "link": url_list[r],
                "pub_date": arrow.get(date_list[r]),
            }
            for r in range(len(title_list))
        ],
    }
