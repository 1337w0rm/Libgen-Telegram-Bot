# -*- coding: utf-8 -*-

import re, os,wget
import urllib.error
import urllib.parse
import urllib.request
import requests
from bs4 import BeautifulSoup

from common import LIBGEN_DOMAIN


class BookInfo:
    """Class for storing book information"""

    def __init__(self, book):
        self.title = book.get('title', None)
        self.authors = book.get('authors', None)
        self.id = book.get('id', None)
        self.publisher = book.get('publisher', None)
        self.pages = book.get('pages', None)
        self.format = book.get('format', None)
        self.year = book.get('year', None)
        self.language = book.get('language', None)
        self.year = book.get('year', None)
        self.size = book.get('size', None)

        self.download_links = book.get('links', list())

    def __repr__(self):
        return 'BookInfo(author: {}, title: {}...)'.format(self.author, self.title[:15])

    def __str__(self):
        text_str = '''\
Book:
    Id: {id},
    Author: {author},
    Title: {title},
    Pages: {pages},
    Format: {format},
    Size: {size},\
    '''.format(id=self.id,
               author=self.authors,
               title=self.title,
               pages=self.pages,
               format=self.format,
               size=self.size)

        return text_str


class BookInfoProvider:
    """Class which loads book information"""
    URL = LIBGEN_DOMAIN + 'search.php?req={}&open=0&view=simple&phrase=1&column={}'


    def load_book_list(self, search_query, search_type):
        """Loads books with search_query and search_type. Returns list()"""
        search_query = search_query.strip().replace(" ", "+")
        search_query = urllib.parse.quote(search_query)

        request = urllib.request.Request(self.URL.format(search_query, search_type))
        response = urllib.request.urlopen(request)

        soup = BeautifulSoup(response, 'html.parser')
        table = soup.find('table', attrs={'class': 'c'})
        table_rows = table.findAll('tr', recursive=False)[1:]
        book_list = list()
        for row in table_rows[:10]:
            book_list.append(BookInfo(self.__extract_book(row)))

        return book_list

    def __extract_book(self, table_row):
        """Extract book information from piece of html page. Returns dictionary"""
        book = dict()

        domains = table_row.find_all('td')
        it = iter(domains)

        try:
            book['id'] = next(it).contents[0]
            book['authors'] = ''.join([i.text for i in next(it).find_all('a', href=re.compile("author"))])

            # extract some info from Title domain (possible more)
            title_domain = next(it)
            series = title_domain.find('a', href=re.compile("series"))
            book['series'] = series.text if series is not None else None
            book['title'] = title_domain.find('a', href=re.compile("book")).contents[0]

            # Just text fields
            book['publisher'] = next(it).text
            book['year'] = next(it).text
            book['pages'] = next(it).text
            book['language'] = next(it).text
            book['size'] = next(it).text
            book['format'] = next(it).text


            filename = book['title']
            ext = book['format']
            
            # Get download links
            links = list()
            next(it)
            for link in next(it).find_all('a'):
                download_link = self.__get_download_link(link['href'])
                if download_link is not None:
                    links.append(download_link)
            filename = book['title']
            ext = book['format']

            # Just text fields)

            book['links'] = links
            # dl = book['links'][0]
            # print(dl)
            # print('Download')
            # path = filename
            # if not os.path.exists('book'):
            #     os.makedirs('book')

            # #wget.download(dl,'book/' + path)
            # header = {'User-Agent': 'Aditya7069 Telegram Bot'}
            # r = requests.get(url = dl, headers = header)
            # with open('book/' + path.strip('/') + book['id'], 'wb') as f:
            #     f.write(r.content)
            #     f.close()
            # print("Done")


        except Exception as e:
            print('Got error:', e)
            raise (e)
        return book

    def __get_download_link(self, book_link):
        download_link = None
        request = urllib.request.Request(book_link)
        try:
            response = urllib.request.urlopen(request)
            soup = BeautifulSoup(response, 'html.parser')

            long_link = soup.find_all('a', href=True, text='GET')[0]['href']

        except urllib.error.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            # ...
            print('HTTPError: ', e.code)
        except urllib.error.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            # ...
            print('URLError: ', e.reason)
        except Exception as e:
            # this another shit
            print('Some Another error:', e)
        return long_link
