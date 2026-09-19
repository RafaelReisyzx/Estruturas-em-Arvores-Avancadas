
import matplotlib.pyplot as plt



def _binary_positions(root, depth=0, x_counter=None, positions=None, get_left=None, get_right=None):
    if x_counter is None:
        x_counter = [0]
    if positions is None:
        positions = {}
    if root is None:
        return positions
    _binary_positions(get_left(root), depth + 1, x_counter, positions, get_left, get_right)
    positions[id(root)] = (x_counter[0], -depth, root)
    x_counter[0] += 1
    _binary_positions(get_right(root), depth + 1, x_counter, positions, get_left, get_right)
    return positions


def draw_binary_tree(root, get_left, get_right, get_label, title, path, highlight_ids=None):
    positions = _binary_positions(root, get_left=get_left, get_right=get_right)
    fig, ax = plt.subplots(figsize=(max(6, len(positions) * 0.9), 5))
    highlight_ids = highlight_ids or set()

    def draw_edges(node):
        if node is None:
            return
        x1, y1, _ = positions[id(node)]
        for child in (get_left(node), get_right(node)):
            if child is not None:
                x2, y2, _ = positions[id(child)]
                ax.plot([x1, x2], [y1, y2], color="#888888", zorder=1, linewidth=1.5)
                draw_edges(child)
    draw_edges(root)

    for node_id, (x, y, node) in positions.items():
        color = "#ffb703" if node_id in highlight_ids else "#8ecae6"
        ax.scatter([x], [y], s=1400, color=color, edgecolors="#023047", zorder=2)
        ax.text(x, y, get_label(node), ha="center", va="center", fontsize=10, zorder=3)

    ax.set_title(title, fontsize=13)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)



def _multiway_positions(node, get_children, get_label, depth=0, x_counter=None, positions=None, edge_labels=None, parent=None, edge_label=""):
    if x_counter is None:
        x_counter = [0]
    if positions is None:
        positions = {}
    if edge_labels is None:
        edge_labels = []
    children = get_children(node)
    if not children:
        positions[id(node)] = (x_counter[0], -depth, node)
        x_counter[0] += 1
    else:
        xs = []
        for lbl, child in children:
            _multiway_positions(child, get_children, get_label, depth + 1, x_counter, positions, edge_labels, node, lbl)
            xs.append(positions[id(child)][0])
        positions[id(node)] = (sum(xs) / len(xs), -depth, node)
    if parent is not None:
        edge_labels.append((id(parent), id(node), edge_label))
    return positions, edge_labels


def draw_multiway_tree(root, get_children, get_label, title, path, node_size=1300):
    positions, edge_labels = _multiway_positions(root, get_children, get_label)
    fig, ax = plt.subplots(figsize=(max(6, len(positions) * 0.85), 5.5))

    for pid, cid, lbl in edge_labels:
        x1, y1, _ = positions[pid]
        x2, y2, _ = positions[cid]
        ax.plot([x1, x2], [y1, y2], color="#888888", zorder=1, linewidth=1.5)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, lbl, fontsize=9, color="#d00000",
                ha="center", va="center", backgroundcolor="white", zorder=4)

    for node_id, (x, y, node) in positions.items():
        is_end = getattr(node, "is_end", False)
        color = "#ffb703" if is_end else "#8ecae6"
        ax.scatter([x], [y], s=node_size, color=color, edgecolors="#023047", zorder=2)
        lbl = get_label(node)
        if lbl:
            ax.text(x, y, lbl, ha="center", va="center", fontsize=8, zorder=3)

    ax.set_title(title, fontsize=13)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)
