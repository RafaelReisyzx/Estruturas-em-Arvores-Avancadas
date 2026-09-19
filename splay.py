
class SplayNode:
    __slots__ = ("key", "left", "right", "parent")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    def __init__(self):
        self.root = None
        self.size = 0


    def _rotate(self, x: SplayNode):
        p = x.parent
        g = p.parent
        if p.left is x:
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
        p.parent = x
        x.parent = g
        if g:
            if g.left is p:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    def _splay(self, x: SplayNode):
        while x.parent:
            p = x.parent
            g = p.parent
            if g is None:
                self._rotate(x)  # zig
            elif (g.left is p) == (p.left is x):
                self._rotate(p)  # zig-zig
                self._rotate(x)
            else:
                self._rotate(x)  # zig-zag
                self._rotate(x)


    def insert(self, key):
        if self.root is None:
            self.root = SplayNode(key)
            self.size += 1
            return
        node = self.root
        while True:
            if key == node.key:
                self._splay(node)
                return
            elif key < node.key:
                if node.left is None:
                    new_node = SplayNode(key)
                    node.left = new_node
                    new_node.parent = node
                    self._splay(new_node)
                    self.size += 1
                    return
                node = node.left
            else:
                if node.right is None:
                    new_node = SplayNode(key)
                    node.right = new_node
                    new_node.parent = node
                    self._splay(new_node)
                    self.size += 1
                    return
                node = node.right

    def search(self, key) -> bool:
        node = self.root
        last = None
        while node:
            last = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        if last:
            self._splay(last)
        return False

    def _subtree_max(self, node):
        while node.right:
            node = node.right
        return node

    def delete(self, key) -> bool:
        if not self.search(key):
            return False
      
        root = self.root
        left, right = root.left, root.right
        if left:
            left.parent = None
        if right:
            right.parent = None
        if left is None:
            self.root = right
        else:
            max_left = self._subtree_max(left)
            self._splay(max_left)  
            max_left.right = right
            if right:
                right.parent = max_left
            self.root = max_left
        self.size -= 1
        return True

    def get_left(self, node):
        return node.left

    def get_right(self, node):
        return node.right

    def get_label(self, node):
        return str(node.key)
