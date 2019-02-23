from bs4 import BeautifulSoup
from abc import abstractmethod,ABC
from threading import Thread
import urllib.request
import random
import re

gretty_url    = "https://www.gettyimages.com/photos/{{keyword}}?alloweduse=availableforalluses&family=creative&license=rf&phrase={{keyword}}&sort=best#license"
lorum_ipsum   = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
bing_url      = "https://www.bing.com/search?q={{city_name}}+city+wikipedia&go=Search"
yahoo_url     = "https://images.search.yahoo.com/search/images;_ylt=F;_ylc=X?&fr2=sb-top-images.search.yahoo.com&p={{keyword}}"
gretty_hq_url = "https://media.gettyimages.com/photos/picture-id"


class Image_Crawler(ABC):
    def __init__(self):
        self.urls = []
        self.city_name = ""

    def crawl_page(self, url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
            return BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def search(self, keyword):
        pass
    
    def get_random_url(self):
        if len(self.urls)>10:
            return self.urls[0 : 10 ][random.randint(0, 9)]
        elif(len(self.urls)>0):
            return self.urls[0]
        else:
            return "nothing was found"
        
    def get_urls(self, num_of_urls=None):
        if num_of_urls == None:
            num_of_urls = len(self.urls)
        elif num_of_urls > len(self.urls):
            num_of_urls = len(self.urls)

        return self.urls[0 : num_of_urls]

    def get_city_description(self):
        city_name = self.city_name.replace(" ", "%20")
        url       = bing_url.replace("{{city_name}}",city_name)
        crawler   = self.crawl_page(url)
        try:
            desc  = crawler.find("ul", { "class" : "b_vList" }).find("li").find("div")
            return desc.string
        except:
            return lorum_ipsum

class Gretty_Image_Crawler(Image_Crawler):
    def __init__(self,keyword):
        super().__init__()
        self.search(keyword)

    def search(self, keyword):
        self.urls = []
        self.city_name = keyword.replace(" ", "%20")
        url      = gretty_url.replace("{{keyword}}",keyword)
        crawler  = self.crawl_page(url)
        img_tags = crawler.findAll("a", {"class","search-result-asset-link"})
        for tag in img_tags:
            id = tag["data-asset-id"]
            self.urls.append(gretty_hq_url + id)

        print(self.urls[5])
        return self.urls


class Yahoo_Image_Crawler(Image_Crawler):
    def __init__(self, keyword):
        super().__init__()
        self.search(keyword)
    
    def search(self, keyword):
        self.urls = []
        self.city_name = keyword.replace(" ", "%20")
        url      = yahoo_url.replace("{{keyword}}",keyword)
        crawler  = self.crawl_page(url)
        lis  = crawler.findAll("li",{"class":"ld"})
        for li in lis:
            a = li.find("a")
            href = a["href"]
            img_url = re.search(r'imgurl=(.*?)&rurl', href).group(1)
            img_url = img_url.replace("%2F", "/")
            self.urls.append(img_url)

# def get_array_of_crawlers(num):
#     crawlers = []
#     for i in range(num):
#         cr = Gretty_Image_Crawler()
#         crawlers.append(cr)
#     return crawlers

# def search_crawlers_with_threads(keywords = [], crawlers=[]):
#     threads  = []
#     crawlers__ = []
#     for i, keyowrd in enumerate(keywords):
#         cr      = crawlers[i]
#         process = Thread(target=cr.search, args= keywords)
#         process.start()
#         threads.append(process)
#         crawlers__.append(cr)

#     for process in threads:
#         process.join()

#     return crawlers__