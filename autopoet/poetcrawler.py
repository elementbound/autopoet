from autopoet.webcrawler import *

def poet_name(poet):
    """
    Return the full name of <poet>. If it's unknown, return a capitalized version
    """

    poet_names = {
        'radnóti': 'Radnóti Miklós',
        'petőfi': 'Petőfi Sándor',
        'tóth': 'Tóth Árpád',
        'kosztolányi': 'Kosztolányi Dezső'
    }

    try:
        return poet_names[poet]
    except KeyError:
        return poet.capitalize()

def get_poet(poet):
    """
    Gather text from a given poet. All known poets are listed in the *available_poets* variable.
    """
    try:
        return _poet_mappings[poet.lower()]()
    except KeyError:
        raise UnknownPoetException('Unknown poet: {0}'.format(poet.capitalize()))

def gather(crawler, sources):
    for source in sources:
        crawler.crawl(source)

    return '\n\n'.join(crawler.paragraphs)

def get_petőfi():
    crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
    sources = ['http://mek.oszk.hu/01000/01006/html/']

    return (crawler, sources)

def get_radnóti():
    crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
    sources = [
        # 'http://www.mek.iif.hu/porta/szint/human/szepirod/magyar/radnoti/',
        'http://mek.oszk.hu/01000/01018/01018.htm'
    ]

    return (crawler, sources)

def get_tóth():
    crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
    sources = ['http://mek.oszk.hu/01100/01112/01112.htm']

    return (crawler, sources)

def get_kosztolányi():
    crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
    sources = ['http://mek.oszk.hu/00700/00753/html/']

    return (crawler, sources)

_poet_mappings = {
    'radnóti': get_radnóti,
    'petőfi': get_petőfi,
    'tóth': get_tóth,
    'kosztolányi': get_kosztolányi
}

available_poets = list(_poet_mappings.keys())
