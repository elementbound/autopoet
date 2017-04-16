from autopoet.webcrawler import *

def gather_poet(poet):
    """
    Gather text from a given poet. All known poets are listed in the *available_poets* variable.
    """
    try:
        return _poet_mappings[poet.lower()]()
    except KeyError:
        raise UnknownPoetException('Unknown poet: {0}'.format(poet.capitalize()))

def gather_petőfi():
    crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
    crawler.crawl('http://mek.oszk.hu/01000/01006/html/')

    return '\n\n'.join(crawler.paragraphs)

def gather_radnóti():
    crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
    crawler.crawl('http://mek.oszk.hu/01000/01018/01018.htm')
    crawler.crawl('http://www.mek.iif.hu/porta/szint/human/szepirod/magyar/radnoti/')

    return '\n\n'.join(crawler.paragraphs)

_poet_mappings = {
    'petőfi': gather_petőfi,
    'radnóti': gather_radnóti
}

available_poets = list(_poet_mappings.keys())