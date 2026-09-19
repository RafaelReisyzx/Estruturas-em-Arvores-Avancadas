
import math


class KDNode:
    __slots__ = ("point", "axis", "left", "right")

    def __init__(self, point, axis):
        self.point = point
        self.axis = axis
        self.left = None
        self.right = None


class KDTree:
    def __init__(self, k=2):
        self.k = k
        self.root = None
        self.size = 0

    def insert(self, point):
        self.root = self._insert(self.root, point, 0)
        self.size += 1

    def _insert(self, node, point, depth):
        if node is None:
            return KDNode(point, depth % self.k)
        axis = node.axis
        if point[axis] < node.point[axis]:
            node.left = self._insert(node.left, point, depth + 1)
        else:
            node.right = self._insert(node.right, point, depth + 1)
        return node

    def search(self, point) -> bool:
        node = self.root
        while node:
            if node.point == point:
                return True
            axis = node.axis
            node = node.left if point[axis] < node.point[axis] else node.right
        return False

    def nearest_neighbor(self, target):
        best = [None, math.inf]

        def dist2(a, b):
            return sum((a[i] - b[i]) ** 2 for i in range(self.k))

        def recurse(node):
            if node is None:
                return
            d = dist2(node.point, target)
            if d < best[1]:
                best[0], best[1] = node.point, d
            axis = node.axis
            diff = target[axis] - node.point[axis]
            near, far = (node.left, node.right) if diff < 0 else (node.right, node.left)
            recurse(near)
            if diff ** 2 < best[1]:
                recurse(far)

        recurse(self.root)
        return best[0]

    def range_search(self, low, high):
        
        result = []

        def in_range(p):
            return all(low[i] <= p[i] <= high[i] for i in range(self.k))

        def recurse(node):
            if node is None:
                return
            if in_range(node.point):
                result.append(node.point)
            axis = node.axis
            if low[axis] <= node.point[axis]:
                recurse(node.left)
            if high[axis] >= node.point[axis]:
                recurse(node.right)

        recurse(self.root)
        return result

    def delete(self, point) -> bool:
        self.root, deleted = self._delete(self.root, point, 0)
        if deleted:
            self.size -= 1
        return deleted

    def _find_min(self, node, target_axis, depth):
        if node is None:
            return None
        axis = node.axis
        if axis == target_axis:
            if node.left is None:
                return node
            return self._find_min(node.left, target_axis, depth + 1)
        candidates = [node]
        for child in (node.left, node.right):
            m = self._find_min(child, target_axis, depth + 1)
            if m is not None:
                candidates.append(m)
        return min(candidates, key=lambda n: n.point[target_axis])

    def _delete(self, node, point, depth):
        if node is None:
            return None, False
        axis = node.axis
        if node.point == point:
            if node.right is not None:
                min_node = self._find_min(node.right, axis, depth + 1)
                node.point = min_node.point
                node.right, _ = self._delete(node.right, min_node.point, depth + 1)
            elif node.left is not None:
                min_node = self._find_min(node.left, axis, depth + 1)
                node.point = min_node.point
                node.right, _ = self._delete(node.left, min_node.point, depth + 1)
                node.left = None
            else:
                return None, True
            return node, True
        if point[axis] < node.point[axis]:
            node.left, deleted = self._delete(node.left, point, depth + 1)
        else:
            node.right, deleted = self._delete(node.right, point, depth + 1)
        return node, deleted


    def get_left(self, node):
        return node.left

    def get_right(self, node):
        return node.right

    def get_label(self, node):
        return str(node.point)

    def collect_regions(self, bounds):
       
        regions = []

        def recurse(node, b):
            if node is None:
                return
            x0, x1, y0, y1 = b
            if node.axis == 0:
                regions.append(("v", node.point[0], y0, y1, node.point))
                recurse(node.left, (x0, node.point[0], y0, y1))
                recurse(node.right, (node.point[0], x1, y0, y1))
            else:
                regions.append(("h", node.point[1], x0, x1, node.point))
                recurse(node.left, (x0, x1, y0, node.point[1]))
                recurse(node.right, (x0, x1, node.point[1], y1))

        recurse(self.root, bounds)
        return regions
