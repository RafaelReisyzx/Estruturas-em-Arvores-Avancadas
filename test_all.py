import random
from trie import Trie
from patricia import PatriciaTrie
from splay import SplayTree
from treap import Treap
from kdtree import KDTree

words = ["casa", "carro", "carta", "cartaz", "cão", "caminho", "camisa", "cor", "corda"]

t = Trie()
for w in words:
    t.insert(w)
assert all(t.search(w) for w in words)
assert not t.search("car")
assert t.starts_with("car")
t.delete("carta")
assert not t.search("carta")
assert t.search("cartaz")
print("Trie OK, palavras:", sorted(t.all_words()))

p = PatriciaTrie()
for w in words:
    p.insert(w)
assert all(p.search(w) for w in words), [w for w in words if not p.search(w)]
assert not p.search("car")
p.delete("carta")
assert not p.search("carta")
assert p.search("cartaz")
print("Patricia OK, palavras:", sorted(p.all_words()))
assert sorted(p.all_words()) == sorted(t.all_words())

random.seed(42)
keys = random.sample(range(1, 1000), 30)
s = SplayTree()
for k in keys:
    s.insert(k)
for k in keys:
    assert s.search(k)
assert not s.search(-5)
random.shuffle(keys)
removed = keys[:10]
for k in removed:
    assert s.delete(k)
for k in removed:
    assert not s.search(k)
for k in keys[10:]:
    assert s.search(k)
print("Splay OK, tamanho final:", s.size)

tr = Treap(seed=7)
for k in keys[10:]:
    tr.insert(k)
for k in keys[10:]:
    assert tr.search(k)
extra_removed = keys[10:20]
for k in extra_removed:
    assert tr.delete(k)
for k in extra_removed:
    assert not tr.search(k)
print("Treap OK, tamanho final:", tr.size)

random.seed(1)
pts = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(40)]
kd = KDTree()
for pt in pts:
    kd.insert(pt)
assert all(kd.search(pt) for pt in pts)
nn = kd.nearest_neighbor((50, 50))
print("KD-Tree OK, vizinho mais proximo de (50,50):", nn)
rng = kd.range_search((20, 20), (60, 60))
print("KD-Tree range_search count:", len(rng))
to_remove = pts[:5]
for pt in to_remove:
    assert kd.delete(pt)
for pt in to_remove:
    assert not kd.search(pt)
print("KD-Tree delete OK, tamanho final:", kd.size)

print("\nTODOS OS TESTES PASSARAM")
