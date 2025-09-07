#include "WeightedGraph.h"
#include "Kruskal.h"

#include <iostream>
#include <iomanip>

int main(void)
{
    WeightedGraph g(6);
    auto addEdge = [&g] (unsigned int u, unsigned int v, double w) {
        g.addEdge(u-1, v-1, w);
    };

    addEdge(1, 2, 2);
    addEdge(1, 2, 2);
    addEdge(1, 3, 1);
    addEdge(1, 4, 8);
    addEdge(2, 3, 3);
    addEdge(2, 5, 11);
    addEdge(2, 6, 7);
    addEdge(3, 4, 9);
    addEdge(3, 5, 6);
    addEdge(4, 5, 1);
    addEdge(4, 6, 4);
    addEdge(5, 6, 5);

    Kruskal k(g);
    std::cout << "The minimum spanning tree (MST) of the given graph has\n"
        << "a total weight of " << k.totalWeight()
        << " and consists of the following edges:\n";
    unsigned int counter = 0;
    for (auto& e : k.mstEdges())
        std::cout << std::setw(2) << ++counter << ". v" << (e->p.first + 1)
            << " - v" << (e->p.second + 1) << "\n";

    return 0;
}
