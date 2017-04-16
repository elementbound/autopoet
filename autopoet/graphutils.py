import autopoet.graph

def graph_from_words(words):
    word_pairs = [(words[i], words[i+1]) for i, w in enumerate(words[0:-1])]

    links = {}
    for idx, word_pair in enumerate(word_pairs):
        word_from, word_to = word_pair
        link = autopoet.graph.WeightedLink(word_from, word_to)

        try:
            links[link] += 1
        except KeyError:
            links[link] = 1

    graph = autopoet.graph.WeightedGraph()
    for link, weight in links.items():
        link.weight = weight

        graph.add_node(link.from_node)
        graph.add_node(link.to_node)
        graph.add_link(link)

    return graph 
