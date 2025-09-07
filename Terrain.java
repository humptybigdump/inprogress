package edu.kit.kastel.model;

import java.util.ArrayList;
import java.util.List;

/**
 * This class represents the Mars map that the rover is driving on.
 *
 * @author uezxa
 * @author udkdm
 */
public class Terrain {
    private final int width;
    private final int height;
    private final List<TerrainNode> graph;

    /**
     * Constructs a new Mars map.
     *
     * @param width The width of the Mars map
     * @param height The width of the Mars map
     * @param graph The infrastructure of the Mars map
     */
    public Terrain(int width, int height, List<TerrainNode> graph) {
        this.width = width;
        this.height = height;
        this.graph = new ArrayList<>(graph);
    }

    /**
     * Gets a node by its position on the terrain.
     *
     * @param position The position of the node
     * @return The node object at the given position or null if no node with this position exists
     */
    public Node getNodeByPosition(Vector2D position) {
        for (Node node : this.graph) {
            if (node.getPosition().equals(position)) {
                return node;
            }
        }
        return null;
    }

    /**
     * Gets the destination on the terrain.
     *
     * @return The destination node
     */
    public Node getDestination() {
        for (Node node : this.graph) {
            if (node.isDestination()) {
                return node;
            }
        }
        return null;
    }

    /**
     * Converts the graph into a char array with its representations.
     *
     * @return The graph into a char array with its representations
     */
    public char[][] asArray() {
        char[][] representations = new char[this.height][this.width];
        for (TerrainNode node : this.graph) {
            representations[node.getPosition().getY()][node.getPosition().getX()] = node.getRepresentation();
        }
        return representations;
    }
}
