import time, random, string, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from trie import Trie
from patricia import PatriciaTrie
from splay import SplayTree
from treap import Treap
from kdtree import KDTree

FIG = "../figures/"
import os
os.makedirs(FIG, exist_ok=True)
random.seed(0)

def random_word(length=8):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

SIZES = [500, 1000, 2000, 4000, 8000, 16000]

# ================= Experimento 1: Trie vs Patricia (strings aleatorias) =================
results_str = {"n": SIZES, "trie_insert": [], "patricia_insert": [],
               "trie_search": [], "patricia_search": [], "trie_mem_nodes": [], "patricia_mem_nodes": []}

def count_nodes_trie(node):
    return 1 + sum(count_nodes_trie(c) for c in node.children.values())

def count_nodes_patricia(node):
    return 1 + sum(count_nodes_patricia(c) for _, c in node.children.values())

for n in SIZES:
    words = [random_word() for _ in range(n)]
    search_sample = random.sample(words, min(200, n))

    t0 = time.perf_counter()
    trie = Trie()
    for w in words:
        trie.insert(w)
    results_str["trie_insert"].append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    for w in search_sample:
        trie.search(w)
    results_str["trie_search"].append(time.perf_counter() - t0)
    results_str["trie_mem_nodes"].append(count_nodes_trie(trie.root))

    t0 = time.perf_counter()
    pat = PatriciaTrie()
    for w in words:
        pat.insert(w)
    results_str["patricia_insert"].append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    for w in search_sample:
        pat.search(w)
    results_str["patricia_search"].append(time.perf_counter() - t0)
    results_str["patricia_mem_nodes"].append(count_nodes_patricia(pat.root))

    print(f"[strings] n={n} ok")

# ================= Experimento 2: Splay vs Treap - acesso aleatorio uniforme =================
results_uniform = {"n": SIZES, "splay_insert": [], "treap_insert": [],
                    "splay_search": [], "treap_search": []}

for n in SIZES:
    keys = random.sample(range(n * 10), n)
    search_sample = [random.choice(keys) for _ in range(500)]

    t0 = time.perf_counter()
    sp = SplayTree()
    for k in keys:
        sp.insert(k)
    results_uniform["splay_insert"].append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    for k in search_sample:
        sp.search(k)
    results_uniform["splay_search"].append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    tp = Treap(seed=1)
    for k in keys:
        tp.insert(k)
    results_uniform["treap_insert"].append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    for k in search_sample:
        tp.search(k)
    results_uniform["treap_search"].append(time.perf_counter() - t0)

    print(f"[uniforme] n={n} ok")

# ================= Experimento 3: Splay vs Treap - localidade temporal (80/20) =================
results_locality = {"n": SIZES, "splay_hot": [], "treap_hot": []}

for n in SIZES:
    keys = list(range(n))
    random.shuffle(keys)
    hot_keys = keys[: max(1, n // 20)]  
    accesses = []
    for _ in range(2000):
        if random.random() < 0.8:
            accesses.append(random.choice(hot_keys))
        else:
            accesses.append(random.choice(keys))

    sp = SplayTree()
    for k in keys:
        sp.insert(k)
    t0 = time.perf_counter()
    for a in accesses:
        sp.search(a)
    results_locality["splay_hot"].append(time.perf_counter() - t0)

    tp = Treap(seed=2)
    for k in keys:
        tp.insert(k)
    t0 = time.perf_counter()
    for a in accesses:
        tp.search(a)
    results_locality["treap_hot"].append(time.perf_counter() - t0)

    print(f"[localidade] n={n} ok")

# ================= Experimento 4: KD-Tree - busca por vizinho mais proximo e range search =================
results_kd = {"n": SIZES, "build": [], "nn_query": [], "range_query": []}

for n in SIZES:
    pts = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
    t0 = time.perf_counter()
    kd = KDTree()
    for p in pts:
        kd.insert(p)
    results_kd["build"].append(time.perf_counter() - t0)

    targets = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(200)]
    t0 = time.perf_counter()
    for tg in targets:
        kd.nearest_neighbor(tg)
    results_kd["nn_query"].append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    for _ in range(50):
        lo = (random.uniform(0, 900), random.uniform(0, 900))
        hi = (lo[0] + 100, lo[1] + 100)
        kd.range_search(lo, hi)
    results_kd["range_query"].append(time.perf_counter() - t0)

    print(f"[kdtree] n={n} ok")

# ================= Experimento 5: Splay/BST em pior caso (chaves ja ordenadas) =================
results_worst = {"n": SIZES, "splay_sorted_insert": [], "treap_sorted_insert": []}
for n in SIZES:
    keys = list(range(n))  # ordem crescente: pior caso classico p/ BST simples
    t0 = time.perf_counter()
    sp = SplayTree()
    for k in keys:
        sp.insert(k)
    results_worst["splay_sorted_insert"].append(time.perf_counter() - t0)

    t0 = time.perf_counter()
    tp = Treap(seed=9)
    for k in keys:
        tp.insert(k)
    results_worst["treap_sorted_insert"].append(time.perf_counter() - t0)
    print(f"[pior caso] n={n} ok")



def save_csv(name, data):
    keys = list(data.keys())
    with open(name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for row in zip(*[data[k] for k in keys]):
            writer.writerow(row)

save_csv("results_strings.csv", results_str)
save_csv("results_uniform.csv", results_uniform)
save_csv("results_locality.csv", results_locality)
save_csv("results_kd.csv", results_kd)
save_csv("results_worst.csv", results_worst)


def plot(x, series_dict, title, ylabel, path, logy=False):
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    for label, ys in series_dict.items():
        ax.plot(x, ys, marker="o", label=label)
    ax.set_xlabel("n (numero de elementos)")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if logy:
        ax.set_yscale("log")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)

plot(SIZES, {"Trie": results_str["trie_insert"], "Patricia": results_str["patricia_insert"]},
     "Tempo de insercao: Trie vs Patricia (strings aleatorias)", "tempo (s)", FIG + "graf_insert_strings.png")

plot(SIZES, {"Trie": results_str["trie_search"], "Patricia": results_str["patricia_search"]},
     "Tempo de busca (200 consultas): Trie vs Patricia", "tempo (s)", FIG + "graf_search_strings.png")

plot(SIZES, {"Trie": results_str["trie_mem_nodes"], "Patricia": results_str["patricia_mem_nodes"]},
     "Numero de nos alocados: Trie vs Patricia", "quantidade de nos", FIG + "graf_nodes_strings.png")

plot(SIZES, {"Splay": results_uniform["splay_insert"], "Treap": results_uniform["treap_insert"]},
     "Tempo de insercao (acesso uniforme): Splay vs Treap", "tempo (s)", FIG + "graf_insert_uniform.png")

plot(SIZES, {"Splay": results_uniform["splay_search"], "Treap": results_uniform["treap_search"]},
     "Tempo de busca uniforme (500 consultas): Splay vs Treap", "tempo (s)", FIG + "graf_search_uniform.png")

plot(SIZES, {"Splay": results_locality["splay_hot"], "Treap": results_locality["treap_hot"]},
     "Busca com localidade temporal (80% em 5% das chaves)", "tempo (s), 2000 consultas", FIG + "graf_locality.png")

plot(SIZES, {"Splay (ordenado)": results_worst["splay_sorted_insert"],
             "Treap (ordenado)": results_worst["treap_sorted_insert"]},
     "Insercao de chaves ja ordenadas (pior caso p/ BST simples)", "tempo (s)", FIG + "graf_worstcase.png")

plot(SIZES, {"Construcao": results_kd["build"]},
     "KD-Tree: tempo de construcao", "tempo (s)", FIG + "graf_kd_build.png")

plot(SIZES, {"Vizinho mais proximo (200 consultas)": results_kd["nn_query"],
             "Busca por intervalo (50 consultas)": results_kd["range_query"]},
     "KD-Tree: tempo de consulta", "tempo (s)", FIG + "graf_kd_query.png")

print("\nEXPERIMENTOS CONCLUIDOS")
for name, r in [("strings", results_str), ("uniform", results_uniform),
                ("locality", results_locality), ("kd", results_kd), ("worst", results_worst)]:
    print(name, r)
