/** @file Kruskal.h */

#ifndef __KRUSKAL_H__
#define __KRUSKAL_H__

#include "WeightedGraph.h"

/**
 * Kruskal's algorithm to construct the minimum spanning tree (MST) of a graph.
 */
class Kruskal
{
    double weight;
    WeightedEdgeList mst;
public:
    /**
     * Construct the minimum spanning tree of the given #WeightedGraph object.
     * @param graph Weighted graph whose MST shall be constructed.
     */
    Kruskal(const WeightedGraph& graph);
    /**
     * Get a read-only reference to the edges that are part of the graph's MST.
     * @return Reference to the #WeightedEdgeList object.
     */
    const WeightedEdgeList& mstEdges() const { return mst; }

    /**
     * Get the total weight of all edges in the MST.
     * @return Sum of all MST edge weights.
     */
    double totalWeight() const { return weight; }
};

#endif
