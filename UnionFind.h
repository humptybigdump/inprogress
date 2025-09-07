/** @file UnionFind.h */

#ifndef __UNION_FIND_H__
#define __UNION_FIND_H__

#include <vector>

/**
 * Union-find data structure (of the weighted quick-union type).
 */
class UnionFind
{
    unsigned int numberOfSets;
    const unsigned int numberOfComponents;
    std::vector<unsigned int> size;
    std::vector<unsigned int> parent;
    unsigned int getRoot(unsigned int x) const;
    void checkInput(unsigned int x) const;
public:
    /**
     * Construct a new union-find object with a given number of components.
     * @param n Number of components that the data structure shall manage.
     */
    UnionFind(unsigned int n);

    /**
     * Get the set index of a given component.
     * @param x Index of the component of interest (between 0 and n-1).
     * @return Index of the set that this component is currently part of.
     */
    unsigned int findSet(unsigned int x) const;

    /**
     * Merge the sets of two given components.
     * @param x Index of a component that is part of the first set.
     * @param y Index of a component that is part of the second set.
     */
    void unionSets(unsigned int x, unsigned int y);

    /**
     * Get the number of components that are part of this data structure.
     * @return Number of components.
     * @note This is equal to the n that was passed to the constructor.
     */
    unsigned int componentCount() const { return numberOfComponents; }

    /**
     * Get the number of sets that are part of this data structure.
     * @return Number of sets.
     * @note Initially, this is equal to the number that #componentCount()
     *    returns. The value decreases when two disjoint sets are merged.
     */
    unsigned int setCount() const { return numberOfSets; }
};

#endif
