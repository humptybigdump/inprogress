package edu.kit.kastel.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * Represents a node in a graph.
 *
 * @author uezxa
 * @author udkdm
 */
public class TerrainNode implements Node {
    private final char representation;
    private final NodeType type;
    private final Vector2D position;
    private final List<Node> neighbours;

    /**
     * Constructs a new node with no neighbours.
     *
     * @param representation The representation of the node
     * @param type The type of the node
     * @param position The position of the node
     */
    public TerrainNode(char representation, NodeType type, Vector2D position) {
        this.representation = representation;
        this.type = type;
        this.position = position;
        this.neighbours = new ArrayList<>();
    }

    @Override
    public char getRepresentation() {
        return this.representation;
    }

    @Override
    public NodeType getType() {
        return this.type;
    }

    @Override
    public Vector2D getPosition() {
        return this.position;
    }

    @Override
    public void addNeighbour(Node node) {
        this.neighbours.add(node);
    }

    @Override
    public List<Node> getNeighbours() {
        return new ArrayList<>(this.neighbours);
    }

    @Override
    public boolean isDestination() {
        return this.type == NodeType.DESTINATION;
    }

    @Override
    public boolean isObstacle() {
        return this.type == NodeType.OBSTACLE;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (this.getClass() != obj.getClass()) {
            return false;
        }

        Node other = (Node) obj;
        return this.position.equals(other.getPosition());
    }

    @Override
    public int hashCode() {
        return Objects.hash(position);
    }

    @Override
    public String toString() {
        return String.valueOf(this.representation);
    }
}
