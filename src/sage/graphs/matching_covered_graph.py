r"""
Matching covered graphs

This module implements functions and operations pertaining to matching covered graphs.

A *matching* in a graph is a set of pairwise nonadjacent links
(nonloop edges). In other words, a matching in a graph is the edge set of an
1-regular subgraph. A matching is called a *perfect* *matching* if it the
subgraph generated by a set of matching edges spans the graph, i.e. it's the
edge set of an 1-regular spanning subgraph. A connected nontrivial graph is
called *matching* *covered* if each edge participates in some perfect matching.

AUTHORS:

- Janmenjaya Panda (2024-06-14): initial version
"""
# ****************************************************************************
#         Copyright (C) 2024 Janmenjaya Panda <janmenjaya.panda.22@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************
from .graph import Graph

class MatchingCoveredGraph(Graph):
    r"""
    Matching covered graph

    INPUT:

    - ``data`` -- can be any of the following:

      - Empty or ``None`` (throws a :class:`ValueError` as the graph must be nontrival).

      - An arbitrary graph.

    - ``matching`` -- (default: ``None``); a perfect matching of the
      graph, that can be given using any valid input format of
      :class:`~sage.graphs.graph.Graph`.

      If set to ``None``, a matching is computed using the other parameters.

    - ``algorithm`` -- string (default: ``'Edmonds'``); the algorithm to be
      used to compute a maximum matching of the graph among

      - ``'Edmonds'`` selects Edmonds' algorithm as implemented in NetworkX,

      - ``'LP'`` uses a Linear Program formulation of the matching problem.

    - ``solver`` -- string (default: ``None``); specify a Mixed Integer
      Linear Programming (MILP) solver to be used. If set to ``None``, the
      default one is used. For more information on MILP solvers and which
      default solver is used, see the method :meth:`solve
      <sage.numerical.mip.MixedIntegerLinearProgram.solve>` of the class
      :class:`MixedIntegerLinearProgram
      <sage.numerical.mip.MixedIntegerLinearProgram>`.

    - ``verbose`` -- integer (default: ``0``); sets the level of verbosity:
      set to 0 by default, which means quiet (only useful when ``algorithm
      == 'LP'``).

    - ``integrality_tolerance`` -- float; parameter for use with MILP
      solvers over an inexact base ring; see
      :meth:`MixedIntegerLinearProgram.get_values`.

    .. NOTE::

        All remaining arguments are passed to the ``Graph`` constructor

    EXAMPLES:

    Generating an object of the class ``MatchingCoveredGraph`` from the
    provided instance of ``Graph`` without providing any other information::

        sage: G = MatchingCoveredGraph(graphs.PetersenGraph())
        sage: G
        Matching covered petersen graph: graph on 10 vertices
        sage: G = graphs.StaircaseGraph(4)
        sage: H = MatchingCoveredGraph(G)
        sage: H
        Matching covered staircase graph: graph on 8 vertices
        sage: H == G
        True
        sage: G = Graph({0: [1, 2, 3, 4], 1: [2, 5], 2: [5], 3: [4, 5], 4: [5]})
        sage: H = MatchingCoveredGraph(G)
        sage: H
        Matching covered graph on 6 vertices
        sage: H == G
        True
        sage: # needs networkx
        sage: import networkx
        sage: G = Graph(networkx.complete_bipartite_graph(12, 12))
        sage: H = MatchingCoveredGraph(G)
        sage: H
        Matching covered graph on 24 vertices
        sage: H == G
        True
        sage: G = Graph('E|fG', sparse=True)
        sage: H = MatchingCoveredGraph(G)
        sage: H
        Matching covered graph on 6 vertices
        sage: H == G
        True
        sage: # needs sage.modules
        sage: M = Matrix([(0,1,0,0,1,1,0,0,0,0),
        ....:             (1,0,1,0,0,0,1,0,0,0),
        ....:             (0,1,0,1,0,0,0,1,0,0),
        ....:             (0,0,1,0,1,0,0,0,1,0),
        ....:             (1,0,0,1,0,0,0,0,0,1),
        ....:             (1,0,0,0,0,0,0,1,1,0),
        ....:             (0,1,0,0,0,0,0,0,1,1),
        ....:             (0,0,1,0,0,1,0,0,0,1),
        ....:             (0,0,0,1,0,1,1,0,0,0),
        ....:             (0,0,0,0,1,0,1,1,0,0)])
        sage: M
        [0 1 0 0 1 1 0 0 0 0]
        [1 0 1 0 0 0 1 0 0 0]
        [0 1 0 1 0 0 0 1 0 0]
        [0 0 1 0 1 0 0 0 1 0]
        [1 0 0 1 0 0 0 0 0 1]
        [1 0 0 0 0 0 0 1 1 0]
        [0 1 0 0 0 0 0 0 1 1]
        [0 0 1 0 0 1 0 0 0 1]
        [0 0 0 1 0 1 1 0 0 0]
        [0 0 0 0 1 0 1 1 0 0]
        sage: G = Graph(M)
        sage: H = MatchingCoveredGraph(G)
        sage: H == G
        True
        sage: # needs sage.modules
        sage: M = Matrix([(-1, 0, 0, 0, 1, 0, 0, 0, 0, 0,-1, 0, 0, 0, 0),
        ....:             ( 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0),
        ....:             ( 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0, 0),
        ....:             ( 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0),
        ....:             ( 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1),
        ....:             ( 0, 0, 0, 0, 0,-1, 0, 0, 0, 1, 1, 0, 0, 0, 0),
        ....:             ( 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 1, 0, 0, 0),
        ....:             ( 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 1, 0, 0),
        ....:             ( 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 1, 0),
        ....:             ( 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 1)])
        sage: M
        [-1  0  0  0  1  0  0  0  0  0 -1  0  0  0  0]
        [ 1 -1  0  0  0  0  0  0  0  0  0 -1  0  0  0]
        [ 0  1 -1  0  0  0  0  0  0  0  0  0 -1  0  0]
        [ 0  0  1 -1  0  0  0  0  0  0  0  0  0 -1  0]
        [ 0  0  0  1 -1  0  0  0  0  0  0  0  0  0 -1]
        [ 0  0  0  0  0 -1  0  0  0  1  1  0  0  0  0]
        [ 0  0  0  0  0  0  0  1 -1  0  0  1  0  0  0]
        [ 0  0  0  0  0  1 -1  0  0  0  0  0  1  0  0]
        [ 0  0  0  0  0  0  0  0  1 -1  0  0  0  1  0]
        [ 0  0  0  0  0  0  1 -1  0  0  0  0  0  0  1]
        sage: G = Graph(M)
        sage: H = MatchingCoveredGraph(G)
        sage: H == G
        True
        sage: G = Graph([(0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7)])
        sage: H = MatchingCoveredGraph(G)
        sage: H == G
        True
        sage: import igraph                                                      # optional - python_igraph
        sage: G = Graph(igraph.Graph([(0, 1), (0, 3), (1, 2), (2, 3)]))          # optional - python_igraph
        sage: H = MatchingCoveredGraph(G)
        sage: H
        Matching covered graph on 4 vertices

    One may specify a matching::

        sage: P = graphs.PetersenGraph()
        sage: M = P.matching()
        sage: G = MatchingCoveredGraph(P, matching=M)
        sage: G
        Matching covered petersen graph: graph on 10 vertices
        sage: P == G
        True
        sage: G = graphs.TruncatedBiwheelGraph(14)
        sage: M = G.matching()
        sage: H = MatchingCoveredGraph(G, M)
        sage: H
        Matching covered truncated biwheel graph: graph on 28 vertices
        sage: H == G
        True

    TESTS:

    An empty graph is not matching covered::

        sage: G = Graph()
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: the graph is trivial
        sage: G = Graph(None)
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: the graph is trivial
        sage: G = MatchingCoveredGraph()
        Traceback (most recent call last):
        ...
        ValueError: the graph is trivial
        sage: G = MatchingCoveredGraph(None)
        Traceback (most recent call last):
        ...
        ValueError: the graph is trivial

    Providing with a graph that is not connected::

        sage: cycle1 = graphs.CycleGraph(4)
        sage: cycle2 = graphs.CycleGraph(6)
        sage: cycle2.relabel(lambda v: v + 4)
        sage: G = Graph()
        sage: G.add_edges(cycle1.edges() + cycle2.edges())
        sage: len(G.connected_components(sort=False))
        2
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: the graph is not connected

    Make sure that self-loops are not allowed for a matching covered graph::

        sage: P = graphs.PetersenGraph()
        sage: G = MatchingCoveredGraph(P)
        sage: G.allows_loops()
        False
        sage: G.allow_loops(True)
        Traceback (most recent call last):
        ...
        ValueError: loops are not allowed in matching covered graphs
        sage: G.add_edge(0, 0)
        Traceback (most recent call last):
        ...
        ValueError: cannot add edge from 0 to 0 in graph without loops
        sage: H = MatchingCoveredGraph(P, loops=True)
        Traceback (most recent call last):
        ...
        ValueError: loops are not allowed in matching covered graphs

    Make sure that multiple edges are allowed for a matching covered graph (by
    default it is off and can be modified to be allowed)::

        sage: P = graphs.PetersenGraph()
        sage: G = MatchingCoveredGraph(P)
        sage: G
        Matching covered petersen graph: graph on 10 vertices
        sage: G.allows_multiple_edges()
        False
        sage: G.size()
        15
        sage: G.allow_multiple_edges(True)
        sage: G.allows_multiple_edges()
        True
        sage: G.add_edge(next(P.edge_iterator()))
        sage: G.size()
        16
        sage: G
        Matching covered petersen graph: multi-graph on 10 vertices
        sage: H = MatchingCoveredGraph(P, multiedges=True)
        sage: H.allows_multiple_edges()
        True
        sage: H.add_edge(next(P.edge_iterator()))
        sage: H.size()
        16
        sage: H
        Matching covered petersen graph: multi-graph on 10 vertices

    Providing with a connected nontrivial graph free of self-loops that is
    not matching covered::

        sage: G = graphs.CompleteGraph(11)
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered
        sage: G = Graph({0: [1, 6, 11], 1: [2, 4], 2: [3, 5], 3: [4, 5],
        ....:            4: [5], 6: [7, 9], 7: [8, 10], 8: [9, 10], 9: [10],
        ....:            11: [12, 14], 12: [13, 15], 13: [14, 15], 14: [15]})
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered
        sage: # needs networkx
        sage: import networkx
        sage: G = Graph(networkx.complete_bipartite_graph(2, 12))
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered
        sage: G = Graph('F~~~w')
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered
        sage: # needs sage.modules
        sage: M = Matrix([(0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0),
        ....:             (1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ....:             (0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ....:             (0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ....:             (0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ....:             (0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ....:             (1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0),
        ....:             (0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0),
        ....:             (0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0),
        ....:             (0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0),
        ....:             (0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0),
        ....:             (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0),
        ....:             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1),
        ....:             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1),
        ....:             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1),
        ....:             (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0)])
        sage: M
        [0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0]
        [1 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0]
        [0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0]
        [0 0 1 0 1 1 0 0 0 0 0 0 0 0 0 0]
        [0 1 0 1 0 1 0 0 0 0 0 0 0 0 0 0]
        [0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0]
        [1 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0]
        [0 0 0 0 0 0 1 0 1 0 1 0 0 0 0 0]
        [0 0 0 0 0 0 0 1 0 1 1 0 0 0 0 0]
        [0 0 0 0 0 0 1 0 1 0 1 0 0 0 0 0]
        [0 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0]
        [1 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0]
        [0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 1]
        [0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 1]
        [0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 1]
        [0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0]
        sage: G = Graph(M)
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered
        sage: # needs sage.modules
        sage: M = Matrix([(1, 1, 0, 0, 0, 0),
        ....:             (0, 0, 1, 1, 0, 0),
        ....:             (0, 0, 1, 0, 1, 0),
        ....:             (1, 0, 0, 0, 0, 1),
        ....:             (0, 1, 0, 1, 1, 1)])
        sage: G = Graph(M)
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered
        sage: G = Graph([(11, 12), (11, 14), (0, 1), (0, 11), (0, 6), (1, 2),
        ....:            (1, 4), (2, 3), (2, 5), (3, 4), (3, 5), (4, 5),
        ....:            (6, 7), (6, 9), (7, 8), (7, 10), (8, 9), (8, 10),
        ....:            (9, 10), (12, 13), (12, 15), (13, 14), (13, 15),
        ....:            (14, 15)])
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered
        sage: import igraph                                                      # optional - python_igraph
        sage: G = Graph(igraph.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)]))  # optional - python_igraph
        sage: H = MatchingCoveredGraph(G)
        Traceback (most recent call last):
        ...
        ValueError: input graph is not matching covered

    Providing with a wrong matching::

        sage: G = graphs.CompleteGraph(6)
        sage: M = Graph(G.matching())
        sage: M.add_edges([(0, 1), (0, 2)])
        sage: H = MatchingCoveredGraph(G, matching=M)
        Traceback (most recent call last):
        ...
        ValueError: the input is not a matching
        sage: N = Graph(G.matching())
        sage: N.add_edge(6, 7)
        sage: H = MatchingCoveredGraph(G, matching=N)
        Traceback (most recent call last):
        ...
        ValueError: the input is not a matching of the graph
        sage: J = Graph()
        sage: J.add_edges([(0, 1), (2, 3)])
        sage: H = MatchingCoveredGraph(G, matching=J)
        Traceback (most recent call last):
        ...
        ValueError: the input is not a perfect matching of the graph

    Note that data shall be one of empty or ``None`` or an instance of
    ``Graph`` or an instance of ``MatchingCoveredGraph``. Otherwise a
    :class:`ValueError` is returned::

        sage: D = digraphs.Complete(10)
        sage: D
        Complete digraph: Digraph on 10 vertices
        sage: G = MatchingCoveredGraph(D)
        Traceback (most recent call last):
        ...
        ValueError: input data is of unknown type
    """

    def __init__(self, data=None, matching=None, algorithm='Edmonds',
                 solver=None, verbose=0, integrality_tolerance=0.001,
                 *args, **kwds):
        r"""
        Create a matching covered graph, that is a connected nontrivial graph
        wherein each edge participates in some perfect matching

        See documentation ``MatchingCoveredGraph?`` for detailed information.
        """
        if kwds is None:
            kwds = {'loops': False}
        else:
            if 'loops' in kwds and kwds['loops']:
                raise ValueError('loops are not allowed in matching '
                                  'covered graphs')
            kwds['loops'] = False

        if data is None:
            raise ValueError('the graph is trivial')

        elif isinstance(data, MatchingCoveredGraph):
            Graph.__init__(self, data, *args, **kwds)

        elif isinstance(data, Graph):
            Graph.__init__(self, data, *args, **kwds)
            self._upgrade_from_graph(matching=matching, algorithm=algorithm,
                                     solver=solver, verbose=verbose,
                                     integrality_tolerance=
                                     integrality_tolerance)
        else:
            raise ValueError('input data is of unknown type')

    def _upgrade_from_graph(self, matching=None, algorithm='Edmonds',
                            solver=None, verbose=0,
                            integrality_tolerance=0.001):
        """
        Upgrade the given graph to a matching covered graph if eligible

        See documentation ``MatchingCoveredGraph?`` for detailed information.
        """
        try:
            coNP_certificate = False
            check = Graph.is_matching_covered(G=self, matching=matching,
                                              algorithm=algorithm,
                                              coNP_certificate=
                                              coNP_certificate,
                                              solver=solver, verbose=verbose,
                                              integrality_tolerance=
                                              integrality_tolerance)

            if not check:
                raise ValueError("input graph is not matching covered")

        except ValueError as error:
            raise error

    def __repr__(self):
        r"""
        Return a short string representation of the matching covered graph

        EXAMPLES:

        If the string representation of the (matching covered) graph does not
        contain the term 'matching covered', it's used as the prefix::

            sage: G = graphs.CompleteGraph(10)
            sage: H = MatchingCoveredGraph(G)
            sage: H
            Matching covered complete graph: graph on 10 vertices
            sage: G = MatchingCoveredGraph(BipartiteGraph(graphs.HexahedralGraph()))
            sage: G  # An object of the class MatchingCoveredGraph
            Matching covered hexahedron: graph on 8 vertices

        In case the string representation of the (matching covered) graph
        contains the term 'matching covered', the representation remains as it
        is::

            sage: G = graphs.CompleteGraph(10)
            sage: H = MatchingCoveredGraph(G)
            sage: H
            Matching covered complete graph: graph on 10 vertices
            sage: J = MatchingCoveredGraph(H)
            sage: J
            Matching covered complete graph: graph on 10 vertices
            sage: G = BipartiteGraph(MatchingCoveredGraph(graphs.HexahedralGraph()))
            sage: G  # An object of the class BipartiteGraph
            Bipartite hexahedron: graph on 8 vertices
            sage: H = MatchingCoveredGraph(G)
            sage: H  # An object of the class MatchingCoveredGraph
            Matching covered hexahedron: graph on 8 vertices
        """
        s = Graph._repr_(self).lower()
        if "matching covered" in s:
            return s.capitalize()
        return "".join(["Matching covered ", s])

    def allow_loops(self, new, check=True):
        """
        Change whether loops are allowed in (matching covered) graphs

        .. NOTE::

            This method overwrites the
            :meth:`~sage.graphs.generic_graph.GenericGraph.allow_loops` method
            to ensure that loops are forbidden in :class:`~BipartiteGraph`.

        INPUT:

        - ``new`` -- boolean

        - ``check`` -- boolean (default: ``True``); whether to remove existing
          loops from the graph when the new status is ``False``. It is an
          argument in
          :meth:`~sage.graphs.generic_graph.GenericGraph.allow_loops` method
          and is not used in this overwritten one.

        EXAMPLES:

        Petersen graph is matching covered::

            sage: P = graphs.PetersenGraph()
            sage: P.is_matching_covered()
            True
            sage: G = MatchingCoveredGraph(P)
            sage: G.allow_loops(True)
            Traceback (most recent call last):
            ...
            ValueError: loops are not allowed in matching covered graphs
        """
        if new is True:
            raise ValueError('loops are not allowed in matching covered graphs')