from urlparse import urlparse, urlunparse
import re

from bs4 import BeautifulSoup
import requests

from .base import BaseCrawler
from ...models import Entity, Author, AuthorType

class NationalDailyNgCrawler(BaseCrawler):
    NDN_RE = re.compile('(www\.)?nationaldailyng.com')
    ignore_lst = [
        'wabtn_container',
        'fb-root',
        'fbcb_container',
        'td-a-rec td-a-rec-id-content_bottom ',
        'td-a-rec td-a-rec-id-content_inline ']

    def offer(self, url):
        """ Can this crawler process this URL? """
        parts = urlparse(url)
        return bool(self.NDN_RE.match(parts.netloc))

    def validate_attrs(self, attrs):
        """ Validation test to check if an element is on the ignore list. """
        for item in self.ignore_lst:
            if item in attrs.values():
                return False
            if 'class' in attrs:
                for c in attrs['class']:
                    if c == item:
                        return False
        
        return True

    def extract(self, doc, raw_html):
        """ Extract text and other things from the raw_html for this document. """
        super(NationalDailyNgCrawler, self).extract(doc, raw_html)

        soup = BeautifulSoup(raw_html)

        # gather title
        doc.title = self.extract_plaintext(soup.select('.td-main-content .td-post-header .td-post-title h1.entry-title'))

        #gather publish date
        date = self.extract_plaintext(soup.select('.td-main-content .td-post-header .td-post-title .td-post-date time'))
        doc.published_at = self.parse_timestamp(date)

        #gather text and summary
        nodes = soup.select('.td-main-content .td-post-content')
        doc.summary = ''
        doc.text = ''
        for node in nodes[0].contents:
            if not isinstance(node, basestring) and self.validate_attrs(node.attrs):
                doc.text += "\n\n" + node.text.strip() if node.text.strip() else ''
                if len(doc.summary) < 200:
                    doc.summary += "\n\n" + node.text.strip() if node.text.strip() else ''
        doc.text = doc.text.strip()
        doc.summary = doc.summary.strip()
        
        # gather author 
        author = self.extract_plaintext(soup.select('.td-main-content .td-post-header .td-post-title .td-post-author-name a'))
        if author:
            doc.author = Author.get_or_create(author.strip(), AuthorType.journalist())
        else:
            doc.author = Author.unknown()
