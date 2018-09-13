import os
from contextlib import closing
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

from .files import management


THREADS_NUMBER = cpu_count()


class WebCrawler:
    project_name = ''
    base_url = ''
    queue_file = ''
    crawled_file = ''
    queue_set = set()
    crawled_set = set()

    def __init__(self, project_name, base_url):
        WebCrawler.project_name = project_name
        WebCrawler.base_url = base_url
        WebCrawler.queue_file = os.path.join(project_name, 'queue.txt')
        WebCrawler.crawled_file = os.path.join(project_name, 'crawled.txt')
        self.setup()
        print('Started crawling page, it can take a few minutes.')
        self.crawl_page(WebCrawler.base_url)

    @staticmethod
    def setup():
        management.create_project_directory(WebCrawler.project_name)
        management.create_project_files(WebCrawler.project_name, WebCrawler.base_url)

        # load previous search state, if there was any
        WebCrawler.queue_set = management.file_to_set(WebCrawler.queue_file)
        WebCrawler.crawled_set = management.file_to_set(WebCrawler.crawled_file)

    @staticmethod
    def crawl_page(page_url):
        """
        collects links from page_url,
        removes page_url from queue_set,
        adds it to crawled_set,
        updates files with current values
        """
        if page_url not in WebCrawler.crawled_set:
            WebCrawler.collect_links(page_url)
            WebCrawler.queue_set.remove(page_url)
            WebCrawler.crawled_set.add(page_url)
            WebCrawler.update_files()

    @staticmethod
    def collect_links(page_url):
        """
        collects links from page and adds them to queue_set
        """
        try:
            with closing(requests.get(page_url, stream=True)) as resp:
                content = resp.text
        except requests.RequestException as e:
            print(e)
            return None

        soup = BeautifulSoup(content, 'lxml')

        for link in soup.findAll('a'):
            try:
                absolute_url = urljoin(WebCrawler.base_url, link['href'])

                # ignore `fake` links
                if '#' in absolute_url:
                    continue
                if absolute_url in WebCrawler.queue_set or absolute_url in WebCrawler.crawled_set:
                    continue
                if WebCrawler.base_url in absolute_url:
                    WebCrawler.queue_set.add(absolute_url)

            except KeyError:
                continue

    @staticmethod
    def update_files():
        management.set_to_file(WebCrawler.queue_set, WebCrawler.queue_file)
        management.set_to_file(WebCrawler.crawled_set, WebCrawler.crawled_file)


def main():
    project_name = str(input('Project name: '))
    base_url = str(input('Full url to site you\'d like to crawl: '))

    WebCrawler(project_name, base_url)

    pool = ThreadPool(THREADS_NUMBER)
    pool.map(WebCrawler.crawl_page, WebCrawler.queue_set)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
