from graphviz import Digraph
import uuid


condition_symbols = ['=', '>', '<', '>=', '<=']


class Node(object):
    def __init__(self):
        self.id = ""
        self.value = ""
        self.condition = ""
        self.nodes = []
        self.leafs = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_leaf(self, leaf):
        self.leafs.append(leaf)


class Leaf(object):
    def __init__(self):
        self.id = ""
        self.value = ""
        self.condition = ""

class Tree(object):
    def __init__(self):
        self.root = None


def division_tree(lines: list, level: int, condition: str = ""):
    lenght = len(lines)
    sets = []
    set = []

    node = Node()
    node.id = str(uuid.uuid1())

    node.value = lines[0].split()[level]
    index = level + 1
    while lines[0].split()[index] not in condition_symbols:
        node.value = node.value + " " + lines[0].split()[index]
        index += 1

    node.condition = str(condition)

    start_condition = index
    index = 0
    while index < lenght:
        split = lines[index].split()

        if split[-1][-1] != ':':
            sets.append(lines[index])
            leaf = Leaf()
            leaf.id = str(uuid.uuid1())
            leaf.condition = str(split[start_condition] + " " + split[start_condition+1])
            leaf_value = ""
            i = 1
            print(split)
            while split[-i][-1]!= ":" and split[-i][-1]!="]":
                leaf_value = split[-i] +" "+leaf_value
                i += 1
            leaf.value = leaf_value
            node.add_leaf(leaf)
            index += 1
        else :
            set.append(lines[index])
            new_condition = str(split[start_condition] + " " + split[start_condition+1])
            index += 1
            while index < lenght and lines[index].split()[level] == '|':
                set.append(lines[index])
                index += 1
            sets.append(set)
            node_subtree = division_tree(set[1:], level+1, new_condition)
            node.add_node(node_subtree)
            set = []

    return node

def update_dot_leaf(dot: Digraph, leaf: Leaf, parent_id: str):
    dot.node(leaf.id, leaf.value)
    dot.edge(parent_id, leaf.id, label=leaf.condition)
    return dot


def update_dot_node(dot: Digraph, node: Node, parent_id: str=""):
    dot.node(node.id, node.value)
    if parent_id != "":
        dot.edge(parent_id, node.id, label=node.condition)

    for leaf in node.leafs:
        dot = update_dot_leaf(dot, leaf, node.id)

    for child_node in node.nodes:
        dot = update_dot_node(dot, child_node, node.id)

    return dot

def generate_graphviz(tree: Tree):
    dot = Digraph(comment='The Round Table')
    dot = update_dot_node(dot, tree.root)
    return dot


def get_tree_lines(lines: []):
    result = []
    for i in range(11, len(lines)):
        if lines[i] == '\n':
            return result
        result.append(lines[i])
    return []

def test():
    lines = []
    with open('parser_test/result.txt', 'r') as f:
        lines = f.readlines()

    tree1 = Tree()
    select_lines = get_tree_lines(lines)
    tree1.root = division_tree(select_lines, 0)
    print(tree1)
    dot1 = generate_graphviz(tree1)
    print(dot1)

    with open('parser_test/result2.txt', 'r') as f:
        lines = f.readlines()
    tree2 = Tree()
    tree2.root = division_tree(lines[11:34], 0)
    print(tree2)
    dot2 = generate_graphviz(tree2)
    print(dot2)

    with open('parser_test/result3.txt', 'r') as f:
        lines = f.readlines()
    tree3 = Tree()
    tree3.root = division_tree(lines[11:30], 0)
    print(tree3)
    dot3 = generate_graphviz(tree3)
    print(dot3)

    with open('parser_test/result4.txt', 'r') as f:
        lines = f.readlines()
    tree4 = Tree()
    tree4.root = division_tree(lines[11:99], 0)
    print(tree4)
    dot4 = generate_graphviz(tree4)
    print(dot4)

    with open('parser_test/result5.txt', 'r') as f:
        lines = f.readlines()
    tree5 = Tree()
    tree5.root = division_tree(lines[11:20], 0)
    print(tree5)
    dot5 = generate_graphviz(tree5)
    print(dot5)

    with open('parser_test/result6.txt', 'r') as f:
        lines = f.readlines()
    tree6 = Tree()
    tree6.root = division_tree(lines[11:52], 0)
    print(tree6)
    dot6 = generate_graphviz(tree6)
    print(dot6)

    with open('parser_test/result7.txt', 'r') as f:
        lines = f.readlines()
    tree7 = Tree()
    tree7.root = division_tree(lines[11:158], 0)
    print(tree7)
    dot7 = generate_graphviz(tree7)
    print(dot7)

if __name__ == "__main__":
    test()