class Node:
    """
    Class to represent an arbitrary node

    This class is intended to be subclassed and extended with used-data
    """

class Link:
    """
    Class to store a connection between two arbitrary nodes

    This class is intended to be subclassed and extended with used-data
    """

    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

class Graph:
    """
    Class for storing arbitrary graphs.

    Nodes must be Node-like instances.
    Links also have to be Link-like instances.
    """

    def __init__(self):
        self._nodes = set()
        self._links = set()

    def add_node(self, node):
        self._nodes.add(node)

    def add_link(self, link):
        self._links.add(link)

    # TODO: What am I exactly accomplishing here?
    @property
    def nodes(self):
        return self._nodes

    @property
    def links(self):
        return self._links

    def links_from(self, node):
        """
        Return a list with all links originating from <node>
        """

        links = []

        for link in self.links:
            if link.from_node == node:
                links.append(link)

        return links

class WeightedLink(Link):
    """
    Link class with weight
    """

    def __init__(self, from_node, to_node, weight=1):
        super().__init__(from_node, to_node)
        self.weight = weight

class WeightedGraph(Graph):
    """
    Graph with weighted links
    """
    def normalize_weights(self):
        """
        Normalize all link weights to ]0,1].

        Note: this function assumes positive, non-zero weights
        """

        sums = {}

        for link in self.links:
            try:
                sums[link.from_node] += link.weight
            except KeyError:
                sums[link.from_node] = link.weight

        for link in self.links:
            link.weight /= sums[link.from_node]

    def get_most_probable(self, node):
        """
        Get most probable destination from <node>
        """

        links = self.links_from(node)
        links = sorted(links, key='weight', reverse=True)
        return links[0].to_node

    def get_weighted_random(self, node):
        """
        Get a random destination from <node>
        The heavier a link, the higher chance it has
        """

        import random

        links = self.links_from(node)
        sum_weight = sum([link.weight for link in links])

        at = random.uniform(0, sum_weight)
        for link in links:
            at -= link.weight

            if at <= 0:
                return link.to_node
