
class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.n_words = 0

    def insert(self, word: str):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        if not node.is_end:
            self.n_words += 1
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, s: str):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def delete(self, word: str) -> bool:
        path = []
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            path.append((node, ch))
            node = node.children[ch]
        if not node.is_end:
            return False
        node.is_end = False
        self.n_words -= 1
        for parent, ch in reversed(path):
            child = parent.children[ch]
            if not child.children and not child.is_end:
                del parent.children[ch]
            else:
                break
        return True

    def all_words(self):
        out = []
        def dfs(node, prefix):
            if node.is_end:
                out.append(prefix)
            for ch, child in sorted(node.children.items()):
                dfs(child, prefix + ch)
        dfs(self.root, "")
        return out


    def get_children(self, node):
        return [(ch, child) for ch, child in sorted(node.children.items())]

    def get_label(self, node):
        return ""  
