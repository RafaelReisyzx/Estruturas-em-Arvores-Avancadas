
import random


class TreapNode:
    __slots__ = ("key", "priority", "left", "right")

    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.random()
        self.left = None
        self.right = None


class Treap:
    def __init__(self, seed=None):
        self.root = None
        self.size = 0
        self._rng = random.Random(seed)

    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def insert(self, key):
        priority = self._rng.random()
        self.root, inserted = self._insert(self.root, key, priority)
        if inserted:
            self.size += 1

    def _insert(self, node, key, priority):
        if node is None:
            return TreapNode(key, priority), True
        if key == node.key:
            return node, False
        if key < node.key:
            node.left, inserted = self._insert(node.left, key, priority)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right, inserted = self._insert(node.right, key, priority)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)
        return node, inserted

    def search(self, key) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def delete(self, key) -> bool:
        self.root, deleted = self._delete(self.root, key)
        if deleted:
            self.size -= 1
        return deleted

    def _delete(self, node, key):
        if node is None:
            return None, False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete(node.right, key)
            return node, deleted
        # achou o no: precisa remove-lo "descendo-o" via rotacoes ate virar folha
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        if node.left.priority > node.right.priority:
            node = self._rotate_right(node)
            node.right, _ = self._delete(node.right, key)
        else:
            node = self._rotate_left(node)
            node.left, _ = self._delete(node.left, key)
        return node, True


    def get_left(self, node):
        return node.left

    def get_right(self, node):
        return node.right

    def get_label(self, node):
        return f"{node.key}\n({node.priority:.2f})"
