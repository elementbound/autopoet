from pprint import pprint
from autopoet.webcrawler import *
import autopoet.poetcrawler as poetcrawler
import autopoet.utils as utils

def word_histogram(text):
    histogram = {}

    for word in text.split():
        if not word.isalpha():
            continue

        word = word.lower()
        try:
            histogram[word] += 1
        except KeyError:
            histogram[word] = 1

    return histogram

def run(args):
    poet = args.poet if args.poet else poetcrawler.available_poets[0]

    print('Grabbing data for poet', poetcrawler.poet_name(poet))
    crawler, sources = poetcrawler.get_poet(poet)

    text = utils.gather_with_progress(crawler, sources)

    print('Gathered word stats: ')
    words = word_histogram(text)
    sorted_words = [(k, words[k]) for k in sorted(words, key=words.get, reverse=True)]

    print('Top 50 words:')
    for word, count in sorted_words[:50]:
        if count < 10:
            continue

        try:
            print('{0:<32} {1}'.format(word, count))
        except UnicodeEncodeError:
            print('{0:<32} {1}'.format(str(word.encode('utf-8')), count))

    print('Unique words:', len(words))
    print('Words in total:', len(text.split()))
