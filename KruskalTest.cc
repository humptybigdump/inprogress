#include "gtest/gtest.h"
#include "WeightedGraph.h"
#include "Kruskal.h"

#include <limits>

TEST(KruskalTest, NoVertices)
{
    WeightedGraph g(0);
    Kruskal k(g);
    EXPECT_EQ(k.mstEdges().size(), 0);
    EXPECT_DOUBLE_EQ(k.totalWeight(), 0.0);
}

TEST(KruskalTest, NoEdges)
{
    WeightedGraph g(5);
    Kruskal k(g);
    EXPECT_EQ(k.mstEdges().size(), 0);
    EXPECT_DOUBLE_EQ(k.totalWeight(), 0.0);
}

TEST(KruskalTest, PositiveWeights)
{
    WeightedGraph g(6);
    g.addEdge(0, 1, 11.5);
    g.addEdge(0, 3, 2.5);
    g.addEdge(1, 3, 5);
    g.addEdge(2, 4, 8.5);
    g.addEdge(3, 4, 6);
    g.addEdge(4, 5, 3.5);

    Kruskal k(g);
    auto& edges = k.mstEdges();
    EXPECT_EQ(edges.size(), 5);
    EXPECT_DOUBLE_EQ(k.totalWeight(), 25.5);
    for (auto& e : edges)
        if (e->w > 11)
            FAIL();
}

TEST(KruskalTest, NegativeWeights)
{
    WeightedGraph g(4);
    g.addEdge(0, 1, 5);
    g.addEdge(1, 2, 0);
    g.addEdge(2, 3, 2);
    g.addEdge(3, 0, -3);

    Kruskal k(g);
    auto& edges = k.mstEdges();
    EXPECT_EQ(edges.size(), 3);
    EXPECT_DOUBLE_EQ(k.totalWeight(), -1);
    for (auto& e : edges)
        if (e->w > 3)
            FAIL();
}

TEST(KruskalTest, NotConnected)
{
    WeightedGraph g(5);
    g.addEdge(0, 1, 1);
    g.addEdge(2, 3, 1);
    g.addEdge(3, 4, 1);

    Kruskal k(g);
    EXPECT_EQ(k.mstEdges().size(), 3);
    EXPECT_DOUBLE_EQ(k.totalWeight(), 3);
}
