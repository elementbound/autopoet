import autopoet.graph
import autopoet.poetcrawler as poetcrawler

import time

def interval(rest):
    if time.clock() - interval.t_start > rest:
        interval.t_start = time.clock()
        return True
    else:
        return False

interval.t_start = -1

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
    poet = poetcrawler.available_poets[0]
    data = poetcrawler.gather_poet(poet)

    print('Got data for poet', poet.capitalize())
    print('Creating graph... ')

    print('Splitting into words... ')
    words = data.split()
    words = [word.lower() for word in words if word.isalpha()]

    print('Creating word pairs... ')
    word_pairs = [(words[i], words[i+1]) for i, w in enumerate(words[0:-1])]

    print('Got', len(words), 'words and', len(word_pairs), 'pairs')

    graph = autopoet.graph.WordGraph()
    for idx, word_pair in enumerate(word_pairs):
        word_from, word_to = word_pair
        graph.add_node(word_from)
        graph.add_node(word_to)

        if interval(0.1):
            progress = (idx+1)/len(word_pairs)
            s = '[{0:>3}%] {1} -> {2}'.format(int(progress*100), word_from, word_to)
            s = '{0:<64}'.format(s)
            print(s, end='\r')

        graph.add_link(autopoet.graph.WeightedLink(word_from, word_to))

    print('\nNormalizing weights...')
    graph.normalize_weights()

    print('Graph done with', len(graph.nodes), 'words and', len(graph.links), 'links')
    print('Press [Enter] to continue... ')
    input()

    while True:
        clear()

        print('Enter a word, exit with !exit')
        word = input()
        word = word.split()[0].lower()

        if word == '!exit':
            break

        if word not in graph.nodes:
            print('Unknown word:', word)

        links = graph.links_from(word)
        links = sorted(links, key='weight', reverse=True)
        for link in links:
            print('\t{0:<24}: {1:>2}%'.format(link.to_node, int(link.weight*100)))
