import autopoet.graph
import autopoet.poetcrawler as poetcrawler

import time
import random

def interval(rest):
    if time.clock() - interval.t_start > rest:
        interval.t_start = time.clock()
        return True
    else:
        return False

def interval_start():
    interval.t_start = -1

interval_start()

def readline():
    try:
        return input()
    except EOFError:
        return '???'

    import io
    import sys

    istream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    return istream.readline()

def clear():
    import platform
    import os

    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')
    else:
        raise NotImplementedError()

def run():
    poet = random.choice(poetcrawler.available_poets)
    data = poetcrawler.gather_poet(poet)

    print('Got data for poet', poet.capitalize())
    print('Creating graph... ')

    print('Splitting into words... ')
    words = data.split()
    words = [word.lower() for word in words if word.isalpha()]

    print('Creating word pairs... ')
    word_pairs = [(words[i], words[i+1]) for i, w in enumerate(words[0:-1])]

    print('Got', len(words), 'words and', len(word_pairs), 'pairs')

    print('Gathering unique links... ')
    links = {}
    interval_start()
    for idx, word_pair in enumerate(word_pairs):
        word_from, word_to = word_pair
        link = autopoet.graph.WeightedLink(word_from, word_to)

        try:
            links[link] += 1
        except KeyError:
            links[link] = 1

        if interval(0.1):
            progress = (idx+1)/len(word_pairs)
            s = '[{0:>3}%] {1} -> {2}'.format(int(progress*100), word_from, word_to)
            s = '{0:<64}'.format(s)
            print(s, end='\r')

    print('\nAssembling graph... ')
    graph = autopoet.graph.WeightedGraph()
    for link, weight in links.items():
        link.weight = weight

        graph.add_node(link.from_node)
        graph.add_node(link.to_node)
        graph.add_link(link)

    print('Normalizing weights...')
    graph.normalize_weights()

    print('Graph done with', len(graph.nodes), 'words and', len(graph.links), 'links')
    print('Press [Enter] to continue... ')
    readline()

    word = None

    while True:
        clear()

        print('Your current poet is:', poet.capitalize())
        print('Enter a word')
        print('Exit with !exit')
        print('Some random words:', ', '.join(random.sample(graph.nodes, 5)))

        if word is None:
            word = readline()
            continue

        word = word.split()[0].lower()

        if word == '!exit':
            break

        if word not in graph.nodes:
            print('Unknown word:', word)

        print(word)

        links = graph.links_from(word)
        links = sorted(links, key=lambda l: l.weight, reverse=True)
        for link in links:
            print('\t{0:<24}: {1:>2}%'.format(link.to_node, int(link.weight*100)))

        word = readline()
