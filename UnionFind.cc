#include "UnionFind.h"

#include <string>
#include <stdexcept>

UnionFind::UnionFind(unsigned int n)
    : numberOfComponents(n)
    , numberOfSets(n)
{
    size.reserve(n);
    parent.reserve(n);
    for (unsigned int i = 0; i < n; ++i) {
        size.push_back(1);
        parent.push_back(i);
    }
}

unsigned int UnionFind::findSet(unsigned int x) const
{
    checkInput(x);
    return getRoot(x);
}

unsigned int UnionFind::getRoot(unsigned int x) const
{
    while (true) {
        if (x == parent[x])
            return x;
        x = parent[x];
    }
}

void UnionFind::unionSets(unsigned int x, unsigned int y)
{
    checkInput(x);
    checkInput(y);

    unsigned int xSet = getRoot(x);
    unsigned int ySet = getRoot(y);

    if (xSet == ySet)
        return;

    unsigned int sub = (size[xSet] < size[ySet]) ? xSet : ySet;
    unsigned int super = (sub == xSet) ? ySet : xSet;

    --numberOfSets;
    parent[sub] = super;
    size[super] += size[sub];
}

void UnionFind::checkInput(unsigned int x) const
{
    if (x >= numberOfComponents) {
        throw std::invalid_argument(
            "Invalid component index '" + std::to_string(x) + "' received!"
        );
    }
}
