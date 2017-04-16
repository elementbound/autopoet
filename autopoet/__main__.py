from pprint import pprint
from webcrawler import *

def main():
    poet = 'petőfi'

    print('Grabbing data for poet', poet.capitalize())

    if poet == 'petőfi':
        crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
        urls = crawler.crawl('http://mek.oszk.hu/01000/01006/html/')
    elif poet == 'radnóti':
        crawler = build_crawler((CachedWebCrawler, ParagraphCrawler))
        urls = crawler.crawl('http://mek.oszk.hu/01000/01018/01018.htm')
        urls.add(crawler.crawl('http://www.mek.iif.hu/porta/szint/human/szepirod/magyar/radnoti/'))

    print('\n\n')
    pprint(urls)
    print('\n\n')
    print('Gathered word stats: ')
    words = crawler.words
    sorted_words = [(k, words[k]) for k in sorted(words, key=words.get, reverse=True)]

    for word, count in sorted_words:
        try:
            print('{0:<32} {1}'.format(word, count))
        except UnicodeEncodeError:
            print('{0:<32} {1}'.format(str(word.encode('utf-8')), count))

main()
