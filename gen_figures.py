import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from trie import Trie
from patricia import PatriciaTrie
from splay import SplayTree
from treap import Treap
from kdtree import KDTree
from draw_utils import draw_binary_tree, draw_multiway_tree

FIG = "../figures/"


words = ["casa", "carro", "carta", "cartaz", "caminho", "camisa", "cor", "corda"]
t = Trie()
for w in words[:5]:
    t.insert(w)
draw_multiway_tree(t.root, t.get_children, t.get_label,
                    "Trie - estado inicial (5 palavras)", FIG + "trie_estado1.png")
for w in words[5:]:
    t.insert(w)
draw_multiway_tree(t.root, t.get_children, t.get_label,
                    "Trie - apos inserir todas as 8 palavras\n(bifurcacao em prefixos compartilhados)",
                    FIG + "trie_estado2.png")
t.delete("cartaz")
draw_multiway_tree(t.root, t.get_children, t.get_label,
                    "Trie - apos remover 'cartaz'", FIG + "trie_estado3.png")

p = PatriciaTrie()
for w in words[:5]:
    p.insert(w)
draw_multiway_tree(p.root, p.get_children, p.get_label,
                    "Patricia - estado inicial (5 palavras, arestas compactadas)",
                    FIG + "patricia_estado1.png")
for w in words[5:]:
    p.insert(w)
draw_multiway_tree(p.root, p.get_children, p.get_label,
                    "Patricia - apos inserir todas as 8 palavras\n(divisao de prefixos: carro/carta/cartaz)",
                    FIG + "patricia_estado2.png")
p.delete("cartaz")
draw_multiway_tree(p.root, p.get_children, p.get_label,
                    "Patricia - apos remover 'cartaz'\n(fusao de nos com filho unico)",
                    FIG + "patricia_estado3.png")


s = SplayTree()
seq = [50, 30, 70, 20, 40, 60, 80, 10]
for k in seq:
    s.insert(k)
draw_binary_tree(s.root, s.get_left, s.get_right, s.get_label,
                  "Splay - apos insercoes sequenciais\n(ultimo inserido, 10, esta na raiz)",
                  FIG + "splay_estado1.png", highlight_ids={id(s.root)})
s.search(80)
draw_binary_tree(s.root, s.get_left, s.get_right, s.get_label,
                  "Splay - apos acessar a chave 80\n(80 e movida para a raiz via rotacoes)",
                  FIG + "splay_estado2.png", highlight_ids={id(s.root)})
s.delete(50)
draw_binary_tree(s.root, s.get_left, s.get_right, s.get_label,
                  "Splay - apos remover a chave 50",
                  FIG + "splay_estado3.png", highlight_ids={id(s.root)})


tr = Treap(seed=3)
for k in [15, 30, 5, 40, 25, 10, 45, 35]:
    tr.insert(k)
draw_binary_tree(tr.root, tr.get_left, tr.get_right, tr.get_label,
                  "Treap - apos insercoes\n(prioridades aleatorias determinam a forma da arvore)",
                  FIG + "treap_estado1.png")
before_root = tr.root.key
tr.insert(2)  
draw_binary_tree(tr.root, tr.get_left, tr.get_right, tr.get_label,
                  "Treap - apos inserir a chave 2\n(rotacoes ocorrem se a nova prioridade for alta)",
                  FIG + "treap_estado2.png")
tr.delete(15)
draw_binary_tree(tr.root, tr.get_left, tr.get_right, tr.get_label,
                  "Treap - apos remover a chave 15\n(no descido via rotacoes ate virar folha)",
                  FIG + "treap_estado3.png")


import random
random.seed(5)
pts = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2), (3, 8)]

def draw_kdtree_space(kd, pts_inserted, title, path, bounds=(0, 10, 0, 10)):
    fig, ax = plt.subplots(1, 2, figsize=(11, 5))
    xs, ys = zip(*pts_inserted)
    ax[0].scatter(xs, ys, color="#023047", zorder=3)
    for x, y in pts_inserted:
        ax[0].annotate(f"({x},{y})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)
    regions = kd.collect_regions(bounds)
    for kind, coord, lo, hi, point in regions:
        if kind == "v":
            ax[0].plot([coord, coord], [lo, hi], color="#ffb703", linewidth=1.5)
        else:
            ax[0].plot([lo, hi], [coord, coord], color="#219ebc", linewidth=1.5)
    ax[0].set_xlim(bounds[0], bounds[1])
    ax[0].set_ylim(bounds[2], bounds[3])
    ax[0].set_title("Particionamento espacial")

    from draw_utils import _binary_positions
    positions = _binary_positions(kd.root, get_left=kd.get_left, get_right=kd.get_right)
    for node_id, (x, y, node) in positions.items():
        for child in (kd.get_left(node), kd.get_right(node)):
            if child is not None:
                x2, y2, _ = positions[id(child)]
                ax[1].plot([x, x2], [y, y2], color="#888888", linewidth=1.5, zorder=1)
        color = "#ffb703" if node.axis == 0 else "#219ebc"
        ax[1].scatter([x], [y], s=1300, color=color, edgecolors="#023047", zorder=2)
        ax[1].text(x, y, kd.get_label(node), ha="center", va="center", fontsize=7, zorder=3)
    ax[1].axis("off")
    ax[1].set_title("Estrutura em arvore (amarelo=corte em x, azul=corte em y)")

    fig.suptitle(title, fontsize=13)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)

kd = KDTree()
inserted = []
for pt in pts[:4]:
    kd.insert(pt)
    inserted.append(pt)
draw_kdtree_space(kd, inserted, "KD-Tree - estado inicial (4 pontos)", FIG + "kdtree_estado1.png")

for pt in pts[4:]:
    kd.insert(pt)
    inserted.append(pt)
draw_kdtree_space(kd, inserted, "KD-Tree - apos inserir os 7 pontos\n(particionamento alternando eixos x/y)",
                   FIG + "kdtree_estado2.png")

kd.delete((5, 4))
inserted.remove((5, 4))
draw_kdtree_space(kd, inserted, "KD-Tree - apos remover o ponto (5,4)", FIG + "kdtree_estado3.png")

print("Figuras geradas com sucesso.")
