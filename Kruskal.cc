#include "Kruskal.h"
#include "UnionFind.h"
#include "WeightedGraph.h"

#include <algorithm>
#include <memory>
#include <iostream>

Kruskal::Kruskal(const WeightedGraph& graph)
    : weight(0)
{
    // Extract all edges from the given graph.
    auto edges = graph.allEdges();

    // Sort the edges by weight.
    std::sort(edges.begin(), edges.end(),
        [] (const WeightedEdgePtr& l, const WeightedEdgePtr& r) -> bool {
            return l->w < r->w;
        }
    );

    // TODO: Initialize the data structure(s) that you need in the loop.
    for (auto& e : edges) {
        // TODO: Determine if `e' is part of the MST. If this is the case,
        // add it to the `mst' list. Update the `weight' member variable
        // whenever this is necessary.

        // Hint 1: e->p.first and e->p.second give you the endpoints of the
        // edge that we currently consider.

        // Hint 2: To achieve the O(E log E) time complexity, you may only
        // execute operations with logarithmic time complexity here. Make
        // use of suitable data structures!

        // Hint 3: You should be able to do this in 10 lines of code or less.
    }
}
