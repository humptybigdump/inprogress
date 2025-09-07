#include "gtest/gtest.h"
#include "WeightedGraph.h"

#include <cmath>
#include <cstring>

class WeightedGraphTest : public ::testing::Test
{
public:
    WeightedGraphTest() : graph(5) {}
protected:
    WeightedGraph graph;
    void SetUp()
    {
        graph.addEdge(0, 2, 4);
        graph.addEdge(2, 3, -3);
        graph.addEdge(0, 3, 1.5);
        graph.addEdge(1, 4, -2.5);
    }
};

TEST_F(WeightedGraphTest, VertexCount)
{
    EXPECT_EQ(graph.vertexCount(), 5);
    graph.addEdge(0, 2, 9);
    EXPECT_EQ(graph.vertexCount(), 5);
}

TEST_F(WeightedGraphTest, EdgeCount)
{
    EXPECT_EQ(graph.edgeCount(), 4);
    graph.addEdge(0, 4, 1);
    EXPECT_EQ(graph.edgeCount(), 5);
}

TEST_F(WeightedGraphTest, IncidenceRelations)
{
    graph.addEdge(2, 0, 0.6);
    unsigned int incidentEdges = 0;
    double totalWeight = 0;
    constexpr unsigned int expectation[] = {2, 0, 0, 1, 0};
    unsigned int counter[5] = {0};
    constexpr unsigned int v = 2;
    for (auto& e : graph.incidentEdges(v)) {
        unsigned int other = (e->p.first == v) ? e->p.second : e->p.first;
        totalWeight += e->w;
        ++counter[other];
        ++incidentEdges;
    }

    EXPECT_TRUE(std::equal(
        std::begin(counter), std::end(counter), std::begin(expectation)
    ));

    EXPECT_DOUBLE_EQ(totalWeight, 1.6);
    EXPECT_EQ(incidentEdges, 3);

    graph.incidentEdges(1);
    EXPECT_EQ(graph.incidentEdges(1).size(), 1);
    graph.addEdge(1, 2, 7.1);
    EXPECT_EQ(graph.incidentEdges(1).size(), 2);
}

TEST_F(WeightedGraphTest, GetAllEdges)
{
    EXPECT_EQ(graph.allEdges().size(), 4);
    graph.addEdge(2, 1, -7.1);
    graph.addEdge(1, 1, 0.5);
    auto edges = graph.allEdges();
    EXPECT_EQ(edges.size(), 6);
    unsigned int selfLoops = 0;
    double totalWeight = 0;
    for (auto &e : edges) {
        totalWeight += e->w;
        if (e->p.first == e->p.second)
            ++selfLoops;

        // Ensure that correct endpoints are returned.
        if (e->w == -7.1) {
            VertexPair firstOption = std::make_pair(2, 1);
            VertexPair secondOption = std::make_pair(1, 2);
            EXPECT_TRUE(e->p == firstOption || e->p == secondOption);
        }
    }

    EXPECT_DOUBLE_EQ(totalWeight, -6.6);
    EXPECT_EQ(selfLoops, 1);
}

TEST_F(WeightedGraphTest, CheckInputs)
{
    EXPECT_THROW(graph.addEdge(5, 0, 0), std::invalid_argument);
    EXPECT_THROW(graph.addEdge(0, 5, 0), std::invalid_argument);
    EXPECT_THROW(graph.addEdge(0, 0, std::nan("42")), std::invalid_argument);
    EXPECT_THROW(graph.incidentEdges(5), std::invalid_argument);
}
