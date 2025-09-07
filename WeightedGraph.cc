#include "WeightedGraph.h"

#include <memory>
#include <string>
#include <stdexcept>
#include <cmath>

#include <iostream>

WeightedGraph::WeightedGraph(unsigned int n)
    : incidenceList(n)
    , numberOfEdges(0)
{

}

void WeightedGraph::addEdge(unsigned int u, unsigned int v, double w)
{
    checkInput(u);
    checkInput(v);

    if (std::isnan(w))
        throw std::invalid_argument("NaN ist not a valid weight!");

    auto edgePtr = std::shared_ptr<WeightedEdge>(
        new WeightedEdge{std::make_pair(u, v), w}
    );

    incidenceList[u].push_back(edgePtr);
    incidenceList[v].push_back(edgePtr);
    ++numberOfEdges;
}

const WeightedEdgeList& WeightedGraph::incidentEdges(unsigned int u) const
{
    checkInput(u);
    return incidenceList[u];
}

WeightedEdgeVector WeightedGraph::allEdges() const
{
    WeightedEdgeVector edges;
    edges.reserve(numberOfEdges);
    for (int i = 0; i < incidenceList.size(); ++i) {
        bool ignoreLoop = false;
        for (auto& e : incidenceList[i]) {
            if (e->p.first == e->p.second) {
                if (!ignoreLoop)
                    edges.push_back(e);
                ignoreLoop = !ignoreLoop;
            } else if (i == e->p.first)
                edges.push_back(e);
        }
    }

    return edges;
}

void WeightedGraph::checkInput(unsigned int u) const
{
    if (u >= incidenceList.size()) {
        throw std::invalid_argument(
            "Invalid vertex index '" + std::to_string(u) + "' received!"
        );
    }
}
