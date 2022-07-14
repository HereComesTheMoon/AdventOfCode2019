import csv


class Node:
    def __init__(self, name: str, nbrs: set['Node', ...], end: bool = False):
        self.name = name
        self.big = name.isupper()
        self.nbrs = nbrs
        self.end = end

    def add(self, nbr):
        self.nbrs.add(nbr)

    def __repr__(self):
        return self.name
        rep = ""
        for x in self.nbrs:
            rep += f"{x.name}, "
        return rep[:-2]

    def __str__(self):
        return self.name

    def find_paths(self, prev: list['Node', ...], goal: 'Node', paths: list[list['Node', ...]]):
        if self == goal:
            paths.append(prev + [self])
            return paths

        for nbr in self.nbrs:
            if nbr.big or nbr not in prev:
                nbr.find_paths(prev + [self], goal, paths)

        return paths

    def find_paths2(self, prev: list['Node', ...], goal: 'Node', paths: list[list['Node', ...]], double: bool):
        if self == goal:
            paths.append(prev + [self])
            return paths
        if double:
            for nbr in self.nbrs:
                if nbr.big or nbr not in prev:
                    nbr.find_paths2(prev + [self], goal, paths, double)
        else:
            for nbr in self.nbrs:
                if nbr.big or nbr not in prev:
                    nbr.find_paths2(prev + [self], goal, paths, double)
                elif nbr.name != 'start':
                        nbr.find_paths2(prev + [self], goal, paths, True)
        return paths



class Graph:
    def __init__(self, nodes: set[Node, ...]):
        self.nodes = nodes

    def __getitem__(self, item):
        if isinstance(item, Node):
            if item in self.nodes:
                return item.nbrs
        if isinstance(item, str):
            return self.get_node_by_name(item).nbrs
        return None

    def get_node_by_name(self, name: str):
        return next(x for x in self.nodes if x.name == name)

    def add_edge(self, a: str, b: str):
        node_a = self.get_node_by_name(a)
        node_b = self.get_node_by_name(b)
        node_a.add(node_b)
        node_b.add(node_a)

    def __repr__(self):
        rep = ""
        for x in self.nodes:
            rep += f"{x.name}: {x.__repr__()}\n"
        return rep
        # return str([(x.name, (x)) for x in self.nodes])


def read(file: str = '12'):
    with open(f"./data/{file}.csv") as f:
        r = csv.reader(f, delimiter='-')
        node_names = set()
        for a, b in r:
            node_names.add(a)
            node_names.add(b)
    nodes = {
        Node(a, set(), a == 'end') for a in node_names
    }
    G = Graph(nodes)
    with open(f'./data/{file}.csv') as f:
        r = csv.reader(f, delimiter='-')
        for a, b in r:
            G.add_edge(a, b)

    return G


def first(G: Graph):
    start = G.get_node_by_name("start")
    end = G.get_node_by_name("end")
    paths = start.find_paths([], end, [])
    print(paths)
    print(len(paths))


def second(G: Graph):
    start = G.get_node_by_name("start")
    end = G.get_node_by_name("end")
    paths = start.find_paths2([], end, [], False)
    print(paths)
    print(len(paths))
print(second(read('12')))