package edu.kit.kastel.model;

import java.util.List;

/**
 * This interface provides functions for nodes in a graph.
 *
 * @author uezxa
 * @author udkdm
 */
public interface Node {
    /**
     * Gets the representation of the node.
     *
     * @return The representation of the node
     */
    char getRepresentation();

    /**
     * Gets the type of the node.
     *
     * @return The type of the node
     */
    NodeType getType();

    /**
     * Gets the position of the node.
     *
     * @return The position of the node
     */
    Vector2D getPosition();

    /**
     * Checks whether the node is the destination.
     *
     * @return True, if the road is the destination, False otherwise
     */
    boolean isDestination();

    /**
     * Checks whether the node is an obstacle.
     *
     * @return True, if the road is an obstacle, False otherwise
     */
    boolean isObstacle();

    /**
     * Adds another node to the neighbours of the node.
     *
     * @param node The neighbour to be added
     */
    void addNeighbour(Node node);

    /**
     * Gets all the neighbours of the current node.
     *
     * @return The neighbours of the current node
     */
    List<Node> getNeighbours();
}
