import networkx as nx

from equitable_coloring.core import procedure_P
from equitable_coloring.utils import check_state
from equitable_coloring.utils import make_params_from_graph

# from .generate_graph import add_harder_constraints
# from .generate_graph import make_graph_from_solver
# from .generate_graph import make_hard_prob
#
# import z3


def test_hard_prob():
    # Tests for two levels of recursion.
    # See test-graphs/a_2_b_3_recurse.png for the nearly-equitable graph.
    num_colors, s = 5, 5

    # edge_vars, constrs, F = make_hard_prob(num_colors=num_colors,
    #                                        num_nodes_each_color=s,
    #                                        a=2)
    # S = z3.Solver()
    # S.add(*constrs)
    # S.check()

    # G = make_graph_from_solver(edge_vars=edge_vars, solver=S, F=F)

    G = nx.Graph()
    G.add_edges_from([(0, 10), (0, 11), (0, 12), (0, 23), (10, 4), (10, 9),
                      (10, 20), (11, 4), (11, 8), (11, 16), (12, 9), (12, 22),
                      (12, 23), (23, 7), (1, 17), (1, 18), (1, 19), (1, 24),
                      (17, 5), (17, 13), (17, 22), (18, 5), (19, 5), (19, 6),
                      (19, 8), (24, 7), (24, 16), (2, 4), (2, 13), (2, 14),
                      (2, 15), (4, 6), (13, 5), (13, 21), (14, 6), (14, 15),
                      (15, 6), (15, 21), (3, 16), (3, 20), (3, 21), (3, 22),
                      (16, 8), (20, 8), (21, 9), (22, 7)])
    F = {node: node // s for node in range(num_colors * s)}
    F[s - 1] = num_colors - 1

    params = make_params_from_graph(G=G, F=F)

    procedure_P(V_minus=0, V_plus=num_colors - 1, **params)
    check_state(**params)


def test_hardest_prob():
    # Tests for two levels of recursion.
    # See test-graphs/a_7_b_3_no-solo.png for the nearly-equitable graph.

    num_colors, s = 10, 4

    # Since this graph takes a while to find/generate, hard-coding it.
    #
    # edge_vars, constrs, F = make_hard_prob(num_colors=num_colors,
    #                                        num_nodes_each_color=s,
    #                                        a=7)

    # # Ensure a' >= b
    # add_harder_constraints(edge_vars=edge_vars, constrs=constrs,
    #                        F=F, a=7, a_prime=3)

    # S = z3.Solver()
    # S.add(*constrs)
    # S.check()

    # G = make_graph_from_solver(edge_vars=edge_vars, solver=S, F=F)

    G = nx.Graph()
    G.add_edges_from(
        [(0, 19), (0, 24), (0, 29), (0, 30), (0, 35), (19, 3), (19, 7), (19, 9),
         (19, 15), (19, 21), (19, 24), (19, 30), (19, 38), (24, 5), (24, 11),
         (24, 13), (24, 20), (24, 30), (24, 37), (24, 38), (29, 6), (29, 10),
         (29, 13), (29, 15), (29, 16), (29, 17), (29, 20), (29, 26), (30, 6),
         (30, 10), (30, 15), (30, 22), (30, 23), (30, 39), (35, 6), (35, 9),
         (35, 14), (35, 18), (35, 22), (35, 23), (35, 25), (35, 27), (1, 20),
         (1, 26), (1, 31), (1, 34), (1, 38), (20, 4), (20, 8), (20, 14), (20, 18),
         (20, 28), (20, 33), (26, 7), (26, 10), (26, 14), (26, 18), (26, 21),
         (26, 32), (26, 39), (31, 5), (31, 8), (31, 13), (31, 16), (31, 17),
         (31, 21), (31, 25), (31, 27), (34, 7), (34, 8), (34, 13), (34, 18),
         (34, 22), (34, 23), (34, 25), (34, 27), (38, 4), (38, 9), (38, 12),
         (38, 14), (38, 21), (38, 27), (2, 3), (2, 18), (2, 21), (2, 28), (2, 32),
         (2, 33), (2, 36), (2, 37), (2, 39), (3, 5), (3, 9), (3, 13), (3, 22),
         (3, 23), (3, 25), (3, 27), (18, 6), (18, 11), (18, 15), (18, 39), (21, 4),
         (21, 10), (21, 14), (21, 36), (28, 6), (28, 10), (28, 14), (28, 16),
         (28, 17), (28, 25), (28, 27), (32, 5), (32, 10), (32, 12), (32, 16),
         (32, 17), (32, 22), (32, 23), (33, 7), (33, 10), (33, 12), (33, 16),
         (33, 17), (33, 25), (33, 27), (36, 5), (36, 8), (36, 15), (36, 16),
         (36, 17), (36, 25), (36, 27), (37, 5), (37, 11), (37, 15), (37, 16),
         (37, 17), (37, 22), (37, 23), (39, 7), (39, 8), (39, 15), (39, 22),
         (39, 23)]
    )
    F = {node: node // s for node in range(num_colors * s)}
    F[s - 1] = num_colors - 1  # V- = 0, V+ = num_colors - 1

    params = make_params_from_graph(G=G, F=F)

    procedure_P(V_minus=0, V_plus=num_colors - 1, **params)
    check_state(**params)
