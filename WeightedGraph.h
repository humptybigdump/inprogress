/** @file WeightedGraph.h */

#ifndef __WEIGHTED_GRAPH_H__
#define __WEIGHTED_GRAPH_H__

#include <utility>
#include <vector>
#include <list>
#include <memory>

/** Type of a pair that holds two vertex indices. */
typedef std::pair<unsigned int, unsigned int> VertexPair;

/**
 * Undirected, weighted edge to connect vertices in a #WeightedGraph.
 */
struct WeightedEdge
{
    VertexPair p; /**< Unordered pair of endpoint vertices. */
    double w; /**< Weight of the edge. */
};

/** Type of a pointer to a weighted edge. */
typedef std::shared_ptr<const WeightedEdge> WeightedEdgePtr;
/** Type of a list of weighted edge pointers. */
typedef std::list<WeightedEdgePtr> WeightedEdgeList;
/** Type of a vector of weighted edge pointers. */
typedef std::vector<WeightedEdgePtr> WeightedEdgeVector;

/**
 * Undirected graph with weighted edges.
 */
class WeightedGraph
{
    unsigned int numberOfEdges;
    std::vector<WeightedEdgeList> incidenceList;
    void checkInput(unsigned int u) const;
public:
    /**
     * Construct an undirected, weighted graph with a fixed number of vertices.
     * @param n Number of vertices.
     */
    WeightedGraph(unsigned int n);

    /**
     * Add an undirected edge between two vertices of the graph.
     * @param u Index of the first endpoint of the edge (between 0 and n-1).
     * @param v Index of the second endpoint of the edge (between 0 and n-1).
     * @param w Weight of the edge.
     */
    void addEdge(unsigned int u, unsigned int v, double w);

    /**
     * Get all edges incident to a given vertex.
     * @param u Index of the vertex of iterest (between 0 and n-1).
     * @return A read-only reference to the #WeightedEdgeList object.
     * @note Every self-loop appears only once in this list.
     */
    const WeightedEdgeList& incidentEdges(unsigned int u) const;

    /**
     * Get all edges of the graph.
     * @return A new #WeightedEdgeList object.
     */
    WeightedEdgeVector allEdges() const;

    /**
     * Get the number of vertices that are part of the graph.
     * @return Number of vertices.
     * @note This is equal to the n that was passed to the constructor.
     */
    unsigned int vertexCount() const { return incidenceList.size(); }

    /**
     * Get the number of edges that are par of the graph.
     * @return Number of edges.
     */
    unsigned int edgeCount() const { return numberOfEdges; }
};

#endif
