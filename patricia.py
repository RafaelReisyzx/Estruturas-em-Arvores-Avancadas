

class PatriciaNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children = {}  
        self.is_end = False


def _common_prefix_len(a: str, b: str) -> int:
    i = 0
    n = min(len(a), len(b))
    while i < n and a[i] == b[i]:
        i += 1
    return i


class PatriciaTrie:
    def __init__(self):
        self.root = PatriciaNode()
        self.n_words = 0

    def insert(self, word: str):
        node = self.root
        remaining = word
        while True:
            if not remaining:
                if not node.is_end:
                    self.n_words += 1
                node.is_end = True
                return
            first = remaining[0]
            if first not in node.children:
                new_node = PatriciaNode()
                new_node.is_end = True
                node.children[first] = (remaining, new_node)
                self.n_words += 1
                return
            label, child = node.children[first]
            cp = _common_prefix_len(remaining, label)
            if cp == len(label):
                node = child
                remaining = remaining[cp:]
                continue
            split_node = PatriciaNode()
            node.children[first] = (label[:cp], split_node)
            split_node.children[label[cp]] = (label[cp:], child)
            if cp == len(remaining):
                split_node.is_end = True
                self.n_words += 1
                return
            new_leaf = PatriciaNode()
            new_leaf.is_end = True
            split_node.children[remaining[cp]] = (remaining[cp:], new_leaf)
            self.n_words += 1
            return

    def _walk(self, word: str):
       
        node = self.root
        remaining = word
        path = []
        while remaining:
            first = remaining[0]
            if first not in node.children:
                return None, path
            label, child = node.children[first]
            cp = _common_prefix_len(remaining, label)
            if cp != len(label):
                return None, path
            path.append((node, first))
            node = child
            remaining = remaining[cp:]
        return node, path

    def search(self, word: str) -> bool:
        node, _ = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        remaining = prefix
        while remaining:
            first = remaining[0]
            if first not in node.children:
                return False
            label, child = node.children[first]
            cp = _common_prefix_len(remaining, label)
            if cp == len(remaining):
                return True
            if cp != len(label):
                return False
            node = child
            remaining = remaining[cp:]
        return True

    def delete(self, word: str) -> bool:
        node, path = self._walk(word)
        if node is None or not node.is_end:
            return False
        node.is_end = False
        self.n_words -= 1
        for parent, first in reversed(path):
            label, child = parent.children[first]
            if not child.children and not child.is_end:
                del parent.children[first]
            elif len(child.children) == 1 and not child.is_end:
                (only_char, (only_label, only_child)) = next(iter(child.children.items()))
                parent.children[first] = (label + only_label, only_child)
            else:
                break
        return True

    def all_words(self):
        out = []
        def dfs(node, prefix):
            if node.is_end:
                out.append(prefix)
            for ch, (label, child) in sorted(node.children.items()):
                dfs(child, prefix + label)
        dfs(self.root, "")
        return out

 
    def get_children(self, node):
        return [(label, child) for ch, (label, child) in sorted(node.children.items())]

    def get_label(self, node):
        return ""
