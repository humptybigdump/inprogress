#include "gtest/gtest.h"
#include "UnionFind.h"

class UnionFindTest : public ::testing::Test
{
public:
    UnionFindTest() : uf(8) {};
protected:
    UnionFind uf;
};

TEST_F(UnionFindTest, ComponentCount)
{
    EXPECT_EQ(8, uf.componentCount());
    uf.findSet(6);
    EXPECT_EQ(8, uf.componentCount());
    uf.unionSets(3, 4);
    EXPECT_EQ(8, uf.componentCount());
}

TEST_F(UnionFindTest, SetCount)
{
    EXPECT_EQ(8, uf.setCount());
    uf.findSet(1);
    EXPECT_EQ(8, uf.setCount());
    uf.unionSets(0, 1);
    EXPECT_EQ(7, uf.setCount());
    uf.findSet(1);
    EXPECT_EQ(7, uf.setCount());
}

TEST_F(UnionFindTest, CheckInputs)
{
    EXPECT_THROW(uf.findSet(8), std::invalid_argument);
    EXPECT_THROW(uf.unionSets(0, 8), std::invalid_argument);
    EXPECT_THROW(uf.unionSets(8, 0), std::invalid_argument);
}

TEST_F(UnionFindTest, UnionTest)
{
    unsigned int N = 8;
    for (unsigned int i = 0; i < N; ++i)
        for (unsigned int j = 0; j < N; ++j)
            if (i != j)
                EXPECT_NE(uf.findSet(i), uf.findSet(j));
    
    // Ensure that the unionSets operation itself works.
    uf.unionSets(4, 5);
    EXPECT_EQ(uf.findSet(4), uf.findSet(5));

    // Ensure that the smaller subtree is added to the larger one.
    unsigned int setId;
    // 0 has less elements than 4-5. Its parent value should change.
    setId = uf.findSet(4);
    uf.unionSets(0, 4);
    EXPECT_EQ(uf.findSet(0), setId);
    EXPECT_EQ(uf.findSet(4), setId);
    // 6 has less elements than 0-4-5. Its parent value should change.
    setId = uf.findSet(5);
    uf.unionSets(5, 6);
    EXPECT_EQ(uf.findSet(6), setId);
    EXPECT_EQ(uf.findSet(5), setId);
}
