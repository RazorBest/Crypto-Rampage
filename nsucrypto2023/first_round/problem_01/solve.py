import wordsegment as ws

BIGRAMS = "th, he, in, en, nt, re, er, an, ti, es, on, at, se, nd, or, ar, al, te, co, de, to, ra, et, ed, it, sa, em, ro"
BIGRAMS = BIGRAMS.split(',')
BIGRAMS = dict(zip(BIGRAMS, range(0, len(BIGRAMS))))


class Node:
    def __init__(self, data):
        self.data = data
        self.neigh = []

    def add_neighbour(self, node):
        self.neigh.append(node)


def cube_to_graph(cube):
    assert len(cube) == 6

    nodes = [Node(c) for c in cube]
    for i in range(4):
        nodes[i].add_neighbour(nodes[(i - 1) % 4])
        nodes[i].add_neighbour(nodes[(i + 1) % 4])
        nodes[i].add_neighbour(nodes[4])
        nodes[i].add_neighbour(nodes[5])

    for i in range(4, 6):
        for j in range(4):
            nodes[i].add_neighbour(nodes[j])

    return nodes

def bruteforce_graph(node, prefix="", visited=None, chars={}, link=None):
    if visited is None:
        visited = set()
    visited.add(node)

    if len(prefix) == 12:
        for word in ws.UNIGRAMS:
            if len(word) < 6:
                continue
            if word in prefix:
                print(f"Source: {word}")
                print(prefix)
                break
        visited.remove(node)
        return


    for next_node in node.neigh:
        if next_node in visited:
            continue

        bg = node.data + next_node.data

        if bg not in BIGRAMS:
            continue

        if BIGRAMS[bg] < 5000000000:
            continue

        new_prefix = prefix + next_node.data
        bruteforce_graph(next_node, new_prefix, visited, chars=chars, link=link)

    for i, j in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        if node is link[i][j]:
            next_node = link[1 - i][j]
            if next_node not in visited:
                bg = node.data + next_node.data

                if bg not in BIGRAMS:
                    continue

                if BIGRAMS[bg] < 1000000000:
                    continue

                new_prefix = prefix + next_node.data
                bruteforce_graph(next_node, new_prefix, visited, chars=chars, link=link)

    visited.remove(node)

def count_bigrams():
    bigrams = {}
    for word, count in ws.UNIGRAMS.items():
        cprev = word[0]
        for c in word[1:]:
            bigram = cprev + c
            if bigram not in bigrams:
                bigrams[bigram] = 0

            bigrams[bigram] += count
            cprev = c

    return bigrams


def gen_side_pairs(graph):
    pairs = []
    used = []
    for node in graph:
        for next_node in node.neigh:
            if next_node in used:
                continue

            pairs.append((node, next_node))

        used.append(node)

    return pairs


def solve(graph1, graph2):
    global BIGRAMS
    ws.load()
    BIGRAMS = count_bigrams()
    chars = {node.data for node in graph1 + graph2}
    print(len(list(BIGRAMS.items())))

    sides1 = gen_side_pairs(graph1)
    sides2 = gen_side_pairs(graph2)

    for side in sides1:
        for side2 in sides2:
            link = (side, side2)
            for i in range(6):
                bruteforce_graph(graph1[i], prefix=graph1[i].data, chars=chars, link=link)
                bruteforce_graph(graph2[i], prefix=graph2[i].data, chars=chars, link=link)

        for side2 in sides2:
            link = (side, [side2[1], side2[0]])
            for i in range(6):
                bruteforce_graph(graph1[i], prefix=graph1[i].data, chars=chars, link=link)
                bruteforce_graph(graph2[i], prefix=graph2[i].data, chars=chars, link=link)



def main():
    """
    The first cube, projected like this:
        R T S
          A
          I
          E
    """
    cube1 = list("taiers")
    cube2 = list("sanwee")
    graph1 = cube_to_graph(cube1)
    graph2 = cube_to_graph(cube2)

    solve(graph1, graph2)

if __name__ == "__main__":
    main()
