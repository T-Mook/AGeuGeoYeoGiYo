# -*- coding:utf-8 -*-
# import os, sys
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # Add parent folder reference
import requests
from bs4 import BeautifulSoup
from .helpers.trim_text import trim

### Portal News URls ===================================================
# Naver : https://search.naver.com/search.naver?&where=news&query=%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=24&start=11&refresh_start=0
# Daum : https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page=1&q=%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8
# Google : https://www.google.com/search?biw=915&bih=927&tbm=nws&sxsrf=ALeKk038nwBAvApusIKyceqWrZGUALpwkw%3A1609312413703&ei=nSjsX5OiKs2NoASvg52QAw&q=%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8&oq=%EB%B8%94%EB%A1%9D%EC%B2%B4%EC%9D%B8&gs_l=psy-ab.3..0l10.2195.3979.0.4090.13.8.0.1.1.0.171.551.0j4.5.0....0...1c.1j4.64.psy-ab..9.3.315.0...120.f1JHRhHahdw

class search_result_crawler:

    def __init__(self, search_keyword, pages= 5):        

        self.search_keyword = search_keyword
        self.pages = pages # End page number
        print('[ Initialization  ] search_keyword : ', self.search_keyword)

    def run_all(self, confirm= False):

        result_list_naver = self.crawler_naver_total_news()
        result_list_daum = self.crawler_daum_total_news()
        result_list_google = self.crawler_google_total_news()
        result_list_naver_view = self.crawler_naver_view()

        print(result_list_google)
        print(result_list_naver_view)

        self.result = [
            result_list_naver,
            result_list_daum,
            result_list_google,
            result_list_naver_view
        ]

        if confirm:
            print('=== [ Complete: run_all ] ' + ('=' * 50))
            print('Search Keyword: ' + self.search_keyword)
            print('= [ Naver Total News ] ' + ('=' * 50))
            print(result_list_naver[:6])
            print('= [ Daum Total News ] ' + ('=' * 50))
            print(result_list_daum[:6])
            print('= [ Google Total News ] ' + ('=' * 50))
            print(result_list_google[:6])
            print('= [ Google Total News ] ' + ('=' * 50))
            print(result_list_naver_view[:6])

    def soup(self, target_url, parser='html.parser'):
        url = target_url
        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, parser)

            return soup
        
        else : 
            # Not 200
            print(response.status_code)

    def select_specific_prases(self, soup, selector, all= False):
        ''' Using 'select' or 'select_one'
        Search for specific tags and parameters
        and return the results as a list '''

        # soup.select_one('.item_price').get_text()
        # soup.select(selector).get_text()
        if all == False:
            result = soup.select_one(selector)
        else:
            result = soup.select(selector)

        return result

    def url_extractor_from_atag(self, atag, get_params='href'):

        if atag == None:
            result = None

        else:
            result = atag.get(get_params)
            
            ### Trim url in href ===================
            trim_text = trim()
            result = trim_text.pure_url(result)

        return result

    def crawling_with_selectors(self, soup, selectors, target_type):
        select_list = self.select_specific_prases(soup= soup, selector= selectors['total'], all= True)
        
        result_list = []
        for value in select_list:
            ### Check There is content in total selector =========================================
            result_news_title = self.select_specific_prases(soup= value, selector= selectors['title'])

            if result_news_title != None:
                # Classify : Title, Provider, Summary 
                result_news_title = result_news_title.get_text()
                result_news_summary = self.select_specific_prases(soup= value, selector= selectors['summary']).get_text()
                result_news_url = self.select_specific_prases(soup= value, selector= selectors['url'])
                try:
                    # 네이버 VIEW의 경우 파워 광고는 provider가 별도 표시됩니다. 이는 제외합니다. (2021.2.18 기준)
                    result_news_provider = self.select_specific_prases(soup= value, selector= selectors['provider']).get_text()
                except:
                    continue

                # Trim URL
                result_news_url = self.url_extractor_from_atag(atag= result_news_url)

                trimmer = trim()
                if target_type == 'naver_total_news':
                    result_news_provider = trimmer.pure_naver_news_provider(result_news_provider)
                elif target_type == 'daum_total_news':
                    result_news_provider = trimmer.pure_daum_news_provider(result_news_provider)
                else:
                    pass

                ### Contents to List
                # 순서 : 제목, 요약, 제공자, 원문 주소
                result_list.append(
                    [result_news_title, result_news_summary, result_news_provider, result_news_url])
                                
            else:
                pass

        return result_list

    ### === Functions for Each Portals =================================
    # Potal List : Naver, Daum, Google Total News
    ### ================================================================

    def crawler_naver_total_news(self):

        ### Settings ==================================================
        # Selector (기준 2021.1.17) ================================
        selectors = {
            'total': 'div.news_area', # News Info Total CSS Selector # ZINbbc xpd O9g5cc uUPGi
            'title': 'a.news_tit', # News Title CSS Selector
            'provider': 'div.news_info > div.info_group > a.info.press', # News Provider CSS Selector
            'url': 'a.news_tit',
            'summary': 'div.news_dsc > div.dsc_wrap > a.api_txt_lines.dsc_txt_wrap' # News Content Summary CSS Selector
        }

        ### Naver News 페이지 관리 Query (2021.1.27)
        # Naver의 page는 '&start=' query를 통해 관리
        # 1~10이 1page, 11~20이 2page와 같은 규칙성을 갖는다
        # 따라서 10의 자리 숫자만 값을 올려가면서 페이지를 바꿀 수 있다

        result_list = []
        page_tens_digit = 0
        while page_tens_digit < self.pages:
            start_number = (page_tens_digit * 10) + 1 
            url_naver_total_news = 'https://search.naver.com/search.naver?query=' + \
                                    str(self.search_keyword) +  \
                                    '&where=news&ie=utf8&sm=nws_hty' +  \
                                    '&start=' + str(start_number)
            
            ### Crawling =========================================
            soup = self.soup(target_url= url_naver_total_news)
            result_of_page = self.crawling_with_selectors(
                soup= soup, selectors= selectors, target_type= 'naver_total_news')

            result_list = result_list + result_of_page

            page_tens_digit += 1

        return result_list

    def crawler_daum_total_news(self):
        ### Settings  ================================
        # Selector (기준 2021.1.17) ================================
        selectors = {
            'total': 'div.cont_inner', # News Info Total CSS Selector # ZINbbc xpd O9g5cc uUPGi
            'title': 'div.wrap_tit.mg_tit', # News Title CSS Selector
            'provider': 'span.f_nb.date', # News Provider CSS Selector
            'url': 'a[href]',
            'summary': 'p.f_eb.desc' # News Content Summary CSS Selector
        }

        ### Daum News 페이지 관리 Query (2021.1.27)
        # Daum의 page는 '&p=' query를 통해 관리
        # 1이 1page, 2가 2page와 같은 규칙성을 갖는다
        # 따라서 1을 출발로 1의 자리 숫자만 값을 올려가면서 페이지를 바꿀 수 있다

        result_list = []
        page_tens_digit = 1
        while page_tens_digit < (self.pages + 1):
            start_number = page_tens_digit

            url_daum_total_news = 'https://search.daum.net/search?w=news&nil_search=btn&DA=NTB&enc=utf8&cluster=y&cluster_page=1&q=' +  \
                                    str(self.search_keyword) +  \
                                    '&p=' + str(start_number)
            
            ### Crawling =========================================
            soup = self.soup(target_url= url_daum_total_news)
            result_of_page = self.crawling_with_selectors(
                soup= soup, selectors= selectors, target_type= 'daum_total_news')

            result_list = result_list + result_of_page

            page_tens_digit += 1

        return result_list

    def crawler_google_total_news(self):
        ### Settings =====================================================================
        # Selector (기준 2021.1.17) ================================
        selectors = {
            'total': 'div.ZINbbc.xpd.O9g5cc.uUPGi', # News Info Total CSS Selector # ZINbbc xpd O9g5cc uUPGi
            'title': 'div.kCrYT > a > h3 > div', # News Title CSS Selector
            'provider': 'div.kCrYT > a > div.BNeawe.UPmit.AP7Wnd', # News Provider CSS Selector
            'url': 'div.kCrYT > a[href]',
            'summary': 'div.kCrYT > div > div > div > div.BNeawe.s3v9rd.AP7Wnd' # News Content Summary CSS Selector
        }

        ### Google News 페이지 관리 Query (2021.1.27)
        # Google의 page는 '&start=' query를 통해 관리
        # 0~9이 1page, 10~19이 2page와 같은 규칙성을 갖는다
        # 따라서 0을 출발로 10의 자리 숫자만 값을 올려가면서 페이지를 바꿀 수 있다

        result_list = []
        page_tens_digit = 0
        while page_tens_digit < self.pages:
            start_number = page_tens_digit * 10
            url_google_total_news = 'https://www.google.com/search?q=' + \
                str(self.search_keyword) + \
                '&tbm=nws'  + \
                '&start=' + str(start_number)
            
            ### Crawling =========================================
            soup = self.soup(target_url= url_google_total_news)
            result_of_page = self.crawling_with_selectors(
                soup= soup, selectors= selectors, target_type= 'google_total_news')
            
            result_list = result_list + result_of_page

            page_tens_digit += 1

        return result_list


    def crawler_naver_view(self):

        ### Settings ==================================================
        # Selector (기준 2021.2.18) ================================
        selectors = {
            'total': 'div.total_wrap.api_ani_send', # News Info Total CSS Selector # ZINbbc xpd O9g5cc uUPGi
            'title': 'a.api_txt_lines.total_tit', # News Title CSS Selector
            'provider': 'div.total_sub > span > span > span.elss.etc_dsc_inner', # News Provider CSS Selector
            'url': 'div.total_sub > span > span > span.elss.etc_dsc_inner > a[href]',
            'summary': 'div.total_group > div > a > div' # News Content Summary CSS Selector
        }

        ### Naver view 페이지 관리 Query (2021.1.27)
        # 무한 스크롤 방식입니다

        url_naver_view = 'https://search.naver.com/search.naver?where=view&query=' + \
                            str(self.search_keyword)
        
        ### Crawling =========================================
        soup = self.soup(target_url= url_naver_view)
        result_of_page = self.crawling_with_selectors(
            soup= soup, selectors= selectors, target_type= 'url_naver_view')
            
        return result_of_page


if __name__ == '__main__':
    test_word = input('테스트하고자 하는 단어를 입력하세요 (ex. 스마트폰)\n')
    crawler = search_result_crawler(search_keyword= test_word, pages= 2)
    crawler.run_all()
    result = crawler.result

    print('-------[ Complete: TEST ]' + ('-' * 50))
    print('TEST Word: ' + test_word)
    print('Naver Total News:\n', result[0][:3])
    print('Daum Total News:\n', result[1][:3])
    print('Google Total News:\n', result[2][:3])
