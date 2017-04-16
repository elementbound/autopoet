# Patch up import paths a bit
import os
from pathlib import Path

os.chdir(str(Path('.').absolute().parent))

from pprint import pprint
from autopoet.webcrawler import *
import autopoet.poetcrawler as poetcrawler

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

def main():
    poet = 'petőfi'

    print('Grabbing data for poet', poet.capitalize())

    text = poetcrawler.gather_poet(poet)

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

main()
