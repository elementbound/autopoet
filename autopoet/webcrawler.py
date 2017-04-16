import requests
import html.parser
from urllib.parse import urljoin, urlparse, urlunparse
import collections

from pathlib import Path
from hashlib import md5
import json
import base64

import re

class LinkExtractor(html.parser.HTMLParser):
    """
    A simple HTML parser that extracts links from the page.
    **Only <a>'s are considered links!**

    Don't forget to set base_url after reset(), otherwise relative links will fail.
    """

    def reset(self):
        super().reset()

        # self.urls.clear()
        self.urls = []
        self.base_url = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for key, value in attrs:
                if key == 'href':
                    value = urljoin(self.base_url, value)
                    self.urls.append(value)

class ParagraphExtractor(html.parser.HTMLParser):
    """
    Simple HTML parser that will extract text from <p> items.
    Each paragraph is stored in the *paragraphs* list.
    """

    def reset(self):
        super().reset()

        self.paragraphs = []
        self._in_paragraph = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self._in_paragraph += 1

    def handle_endtag(self, tag):
        if tag == 'p':
            self._in_paragraph -= 1

    def handle_data(self, text):
        if self._in_paragraph > 0:
            self.paragraphs.append(text)

class BaseWebCrawler:
    """
    Base for any other web crawler. The BaseWebCrawler downloads a page, extracts links and visits
    those too. It never visits the same URL twice.

    This class is intended for subclassing.
    """

    def check_url(self, url):
        """
        Return whether the URL has to be crawled
        Always return True by default
        """
        return True

    def load_url(self, url):
        """
        Get data from given URL
        A string is expected as output; if you have a bytes object, don't forget to decode
        """

        req = requests.get(url)

        # TODO: Check if req.ok and throw exception
        if not req.ok:
            return ''
        else:
            return req.content.decode(req.encoding)

    def process_url(self, url):
        """
        Modify URL before checking and loading it
        The default behaviour is to drop fragments
        """
        # Parse URL into a list ( tuples are read-only )
        url = list(urlparse(url, 'http'))

        # Remove fragment part
        url[5] = ''

        # Assemble again
        return urlunparse(url)

    def handle_data(self, data):
        """
        Process crawled data
        By default, this does nothing
        """
        pass

    def crawl(self, url):
        """
        Crawl a given URL and all the URLs it links to

        See LinkExtractor
        """

        to_crawl = collections.deque([url])
        visited_urls = set()

        while to_crawl:
            url = to_crawl.pop()
            url = self.process_url(url)

            print('{0} / {1}'.format(len(visited_urls), len(to_crawl)))

            if not self.check_url(url):
                print('SKIP!', url)
                continue

            if url in visited_urls:
                print('SKIP', url)
                continue

            print('GET', url)
            visited_urls.add(url)
            contents = self.load_url(url)

            if contents:
                le = LinkExtractor()
                le.base_url = url
                le.feed(contents)
                self.handle_data(contents)

                new_urls = set(le.urls)
                print('Gathered', len(new_urls), 'URLs')
                to_crawl.extend(new_urls)
            else:
                print('Fail', url)

        return visited_urls

class CachedWebCrawler(BaseWebCrawler):
    """
    Web crawler that will blindly cache site contents into a directory.
    The caching behaviour is **very** simple! No check for modification times or expiration dates;
    if it has an entry for the URL, it will just fetch it from disk.
    """

    def __init__(self, cache_dir='./_crawler_cache'):
        super().__init__()

        self.cache = {}
        self.cache_dir = Path(cache_dir)
        self.cache_index = Path(cache_dir, 'cache.json')

        self.cache_dir.mkdir(exist_ok=True, parents=True)

        try:
            with self.cache_index.open('r', encoding='utf-8') as f:
                self.cache = json.load(f)
        except:
            # Silently let it pass
            pass

    def load_url(self, url):
        # Try fetching it from cache
        try:
            with Path(self.cache_dir, self.cache[url]).open('r', encoding='utf-8') as f:
                return f.read()

            print('Grabbed', url, 'from cache')
        except KeyError:
            # Not cached, fetch it from source
            print('Grabbing', url, 'from source')
            contents = super().load_url(url)

            hash_url = url
            i = 0
            while True:
                hasher = md5()
                hasher.update(hash_url.encode('utf-8'))
                fname = hasher.digest()
                fname = base64.urlsafe_b64encode(fname).decode('ascii')

                if Path(self.cache_dir, fname).exists():
                    i += 1
                    hash_url = '{0}!{1}'.format(i, url)
                else:
                    break

            self.cache[url] = fname
            with Path(self.cache_dir, fname).open('w', encoding='utf-8') as f:
                f.write(contents)

            # Save cache
            with self.cache_index.open('w', encoding='utf-8') as f:
                json.dump(self.cache, f)

            return contents
        except:
            # Fail silently
            return None

class MaskedWebCrawler(BaseWebCrawler):
    """ Crawler that only accepts URLs that match its pattern """

    def __init__(self):
        super().__init__()
        self.pattern = re.compile('.*')

    def check_url(self, url):
        if not super().check_url(url):
            return False

        if self.pattern.match(url) is None:
            print('Rejected URL:', url)

        return self.pattern.match(url) is not None

class ParagraphCrawler(BaseWebCrawler):
    """
    Web crawler that extract paragraph data from sites.

    *paragraphs* stores a list of paragraphs.
    *words* stores a word histogram.
    """

    def __init__(self):
        super().__init__()
        self.paragraphs = []
        self.words = {}

    def handle_data(self, text):
        self.paragraphs.append(text)

        for word in text.split():
            # Only lower-case words
            word = word.lower()

            # Skip words that aren't entirely words
            if not word.isalpha():
                continue

            try:
                self.words[word] += 1
            except KeyError:
                self.words[word] = 1

def build_crawler(base_classes, *args, **kwargs):
    return type('WebCrawler', base_classes, {})(*args, **kwargs)
