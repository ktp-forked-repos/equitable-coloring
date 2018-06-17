import networkx as nx
import numpy as np
from collections import defaultdict


def is_coloring(G, coloring):
    """Determine if the coloring is a valid coloring for the graph G."""
    # Verify that the coloring is valid.
    for (s, d) in G.edges:
        if coloring[s] == coloring[d]:
            return False
    return True


def is_equitable(G, coloring):
    """Determines if the coloring is valid and equitable for the graph G."""

    if not is_coloring(G, coloring):
        return False

    # Verify whether it is equitable.
    color_set_size = defaultdict(int)
    for color in coloring.values():
        color_set_size[color] += 1

    # If there are less then 2 distinct values, the coloring cannot be equitable
    all_set_sizes = set(color_set_size.values())
    if len(all_set_sizes) > 2:
        return False

    a, b = list(all_set_sizes)
    return abs(a - b) <= 1


def change_color(u, X, Y, N, H, F, C):
    """Change the color of 'u' from X to Y and update N, H, F, C."""
    # Change the class of 'u' from X to Y
    F[u] = Y

    # 'u' witnesses and edge from Y -> X instead of from X -> Y now.
    H[(X, Y)] -= 1
    H[(Y, X)] += 1

    for v in G.neighbors(u):
        # 'v' has lost a neighbor in X and gained one in Y
        N[(v, X)] -= 1
        N[(v, Y)] += 1

        if N[(v, X)] == 0:
            # 'v' witnesses F[v] -> X
            H[(F[v], X)] += 1

        if N[(v, Y)] == 1:
            # 'v' no longer witnesses F[v] -> Y
            H[(F[v], Y)] -= 1

    C[X].remove(u)
    C[Y].append(u)


def equitable_color(G, num_colors):
    """Provides equitable (r + 1)-coloring for nodes of G in O(r * n^2) time
     if deg(G) <= r. The algorithm is described in [1]_.

     Attempts to color a graph using r colors, where no neighbors of a node
     can have same color as the node itself and the number of nodes with each
     color differ by at most 1.

     Parameters
     ----------
     G : NetworkX graph

     num_colors : number of colors to use
        This number must be at least one more than the maximum degree of nodes
        in the graph.

     Returns
     -------
     A dictionary with keys representing nodes and values representing
     corresponding coloring.

     Examples
     --------
     >>> from equitable_coloring import equitable_color
     >>> G = nx.cycle_graph(4)
     >>> d = equitable_color(G, num_colors=3)
     >>> d in [{0: 0, 1: 1, 2: 0, 3: 1}, {0: 1, 1: 0, 2: 1, 3: 0}] # TODO: Fix
     False

     References
     ----------
     .. [1] H.A. KIERSTEAD and A.V. KOSTOCHKA: A short proof of the Hajnal-Szemeredi
     theorem on equitable colouring. Combinatorics, Probability and Computing, 17(2),
     (2008), 265-270.
    """

    # Map nodes to integers for simplicity later.
    nodes_to_int = {}
    int_to_nodes = {}

    for idx, node in enumerate(G.nodes):
        nodes_to_int[node] = idx
        int_to_nodes[idx] = node

    G = nx.relabel_nodes(G, nodes_to_int, copy=True)

    # Basic graph statistics and sanity check.
    n_ = len(G)
    r_ = max([G.degree(node) for node in G.nodes], default=0)

    if r_ >= num_colors:
        raise nx.NetworkXAlgorithmError(
            'Graph has maximum degree {}, needs {} (> {}) colors for guaranteed coloring.'
            .format(r_, r_ + 1, num_colors)
        )

    # Irrespective of what the maximum degree of the graph is, we will set r to
    # be the maximum possible degree.
    r = num_colors - 1

    # Ensure that the number of nodes in G is a multiple of (r + 1)
    s = n_ // (r + 1)
    if n_ != s * (r + 1):
        p = (r + 1) - n_ % (r + 1)
        s += 1

        # Complete graph K_p between (imaginary) nodes [n_, ... , n_ + p]
        K = nx.relabel_nodes(nx.complete_graph(p),
                             {idx: idx + n_ for idx in range(p)})
        G.add_edges_from(K.edges)

    n = len(G.nodes)
    colors = list(range(num_colors))

    # Starting the algorithm.
    L = {node: list(G.neighbors(node)) for node in G.nodes}
    L_ = defaultdict(lambda: [])

    # Arbitrary equitable allocation of colors to nodes.
    F = {node: idx % num_colors for idx, node in enumerate(G.nodes)}

    C = defaultdict(lambda: [])
    for node, color in F:
        C[color].append(node)

    # Currently all nodes witness all edges.
    H = {(c1, c2): s for c1 in range(num_colors) for c2 in range(num_colors)}

    # The neighborhood is empty initially.
    N = {(node, color): 0 for node in G.nodes for color in range(num_colors)}

    # Start of algorithm.
    for u in G.nodes:
        for v in G.neighbors(u):
            L_[u].append(v)

            N[(u, F[v])] += 1
            N[(v, F[u])] += 1

            if F[u] != F[v]:
                # Were 'u' and 'v' witnesses for F[u] -> F[v] or F[v] -> F[u]?
                H[F[v], F[u]] -= 1  # v cannot witness an edge between F[v], F[u]
                H[F[u], F[v]] -= 1  # u cannot witness an edge between F[u], F[v]

        if N[(u, F[u])] != 0:
            # Find the first color where 'u' does not have any neighbors.
            Y = [k for k in colors if N[(u, k)] == 0][0]
            X = F[u]
            change_color(u, X, Y, N, H, F, C)

            # Procedure P

            V_minus = X
            V_plus = Y

            A_cal = set()
            T_cal = defaultdict(lambda: [])
            R_cal = []

            # BFS to determine A_cal, i.e. colors reachable from V-
            reachable = [V_minus]
            idx = 0
            while idx < len(reachable):
                pop = reachable[idx]
                idx += 1

                A_cal.add(pop)
                R_cal.append(pop)

                next_layer = [k for k in colors if H[(V_minus, k)] > 0]
                for dst in next_layer:
                    # Record that pop can reach dst
                    T_cal[dst].append(pop)

                reachable.extend([x for x in next_layer if x not in A_cal])

            if V_plus in A_cal:
                # Easy case: V+ is in A_cal
                # Move one node from V+ to V- going through T_cal.
                # TODO
                pass
            else:
                # Rougher case
                pass


