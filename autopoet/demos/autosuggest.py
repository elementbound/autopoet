import autopoet.graph
import autopoet.poetcrawler as poetcrawler

import random

from autopoet.utils import *

def run(args):
    poet = args.poet if args.poet else random.choice(poetcrawler.available_poets)
    print('Grabbing data for poet', poetcrawler.poet_name(poet))
    crawler, sources = poetcrawler.get_poet(poet)
    data = gather_with_progress(crawler, sources)

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

            try:
                print(s, end='\r')
            except UnicodeEncodeError:
                print('wtf?!')

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

        print('Your current poet is:', poetcrawler.poet_name(poet))
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
            # Fuzzy search
            ratios = {w: diff(w, word) for w in graph.nodes}

            ratios = [(k, ratios[k]) for k in sorted(ratios.keys(), key=ratios.get, reverse=True)]
            best_word, best_ratio = ratios[0]

            if best_ratio < 0.25:
                print('Unknown word:', word)
                print('Closest match is', best_word, 'at {0}%'.format(int(best_ratio*100)))
                continue

            word = best_word

        print(word)

        links = graph.links_from(word)
        links = sorted(links, key=lambda l: l.weight, reverse=True)
        for link in links:
            print('\t{0:<24}: {1:>2}%'.format(link.to_node, int(link.weight*100)))

        word = readline()
