import requests
from bs4 import BeautifulSoup
import HeaderMaker

def GetHtml(url) -> str:
    print(f'Get {url}')
    headers = HeaderMaker.Get(url)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    WebContent = response.text
    return WebContent

def GetResult(Path:str) -> dict:
    url = f'https://cn.bing.com{Path}'
    while True:
        WebContent = GetHtml(url)
        WebPage = BeautifulSoup(WebContent, 'html.parser')
        ol_element = WebPage.find('ol', {'id': 'b_results'})
        if ol_element != None:
            ol_elements = ol_element.find_all('li', {'class': 'b_algo'})
            if len(ol_elements) >= 10:
                break
    RepDict = dict()
    RepDict['amount'] = len(ol_elements)
    results = list()
    for li_item in ol_elements:
        tmp_dict = dict()
        OneResult = BeautifulSoup(str(li_item), 'html.parser')
        tmp = OneResult.find('div', {'class': 'b_tpcn'})
        tmp = tmp.find('a', {'class': 'tilk'})
        tmp = tmp.find('div', {'class': 'tptxt'})
        LinkHost = tmp.find('div', {'class': 'tptt'})
        tmp_dict['LinkHost'] = LinkHost.text
        tmp = OneResult.find('h2')
        tmp = tmp.find('a')
        FullLink = tmp['href']
        Title = tmp.text
        tmp_dict['FullLink'] = FullLink
        tmp_dict['Title'] = Title
        tmp = OneResult.find('div', {'class': 'b_caption'})
        describes = tmp.find('p')
        tmp_dict['describes'] = describes.text[2:]
        results.append(tmp_dict)
    RepDict['results'] = results
    return RepDict

def Crawler(Path:str) -> dict:
    while True:
        try:
            RepDict = GetResult(Path)
            return RepDict
        except Exception as e:
            pass