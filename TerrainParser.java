package edu.kit.kastel.model;

import edu.kit.kastel.commands.InvalidCommandArgumentException;

import java.util.ArrayList;
import java.util.List;

/**
 * Parses a string representation of a terrain map.
 * Handles validation, node creation, and connectivity for the terrain graph.
 *
 * @author uezxa
 * @author udkdm
 */
public class TerrainParser {
    private final int width;
    private final int height;
    private final List<TerrainNode> graph;

    private Rover rover;
    private int currentLine = 0;

    /**
     * Constructs a new map parser expecting the width and height of the map.
     *
     * @param width the width of the map
     * @param height the height of the map
     */
    public TerrainParser(int width, int height) {
        this.width = width;
        this.height = height;
        this.graph = new ArrayList<>();
    }

    /**
     * Returns {@code true} iff the parser has valid results, i.e. the parsing
     * finished successfully.
     *
     * @return {@code true} iff the parser has valid results
     */
    public boolean hasValidResult() {
        return hasRover() && hasDestination() && this.graph.size() == this.width * this.height;
    }

    /**
     * Parses one Line into nodes.
     *
     * @param line The line to be parsed
     * @throws InvalidCommandArgumentException If the line could not be parsed
     */
    public void parseLine(String line) throws InvalidCommandArgumentException {
        // Check if the length of the line is equal to the width of the map.
        if (line.length() != this.width) {
            throw new InvalidCommandArgumentException();
        }

        // Iterate through every character in the line where the index i stands for an X coordinate.
        for (int i = 0; i < this.width; i++) {
            char currentCharacter = line.charAt(i);
            // Check if the character is a legal character for the terrain representations.
            if (!NodeType.LEGAL_CHARACTERS.contains(currentCharacter)) {
                throw new InvalidCommandArgumentException();
            }

            // Create a new vector where X is the current index i and Y is the current line that is being parsed.
            Vector2D position = new Vector2D(i, this.currentLine);

            if (currentCharacter == NodeType.ROVER_REPRESENTATION
                    || currentCharacter == NodeType.ROVER_ON_DESTINATION_REPRESENTATION) {
                initializeRover(currentCharacter, position);
            } else if (currentCharacter == NodeType.DESTINATION_REPRESENTATION) {
                initializeDestination(currentCharacter, position);
            } else {
                this.graph.add(new TerrainNode(currentCharacter, NodeType.getFromRepresentation(currentCharacter), position));
            }
        }
        this.currentLine++;
    }

    /**
     * Gets the rover.
     *
     * @return The rover
     */
    public Rover getRover() {
        return this.rover;
    }

    /**
     * Gets the Mars map.
     *
     * @return The Mars map
     */
    public Terrain getMarsMap() {
        connectNodes();
        return new Terrain(this.width, this.height, this.graph);
    }

    private void connectNodes() {
        for (Node node : this.graph) {
            // Skip nodes that are obstacles.
            if (node.isObstacle()) {
                continue;
            }

            for (Direction direction : Direction.values()) {
                Vector2D neighbourPosition = node.getPosition().add(direction.getUnitVector());
                // Find the neighbour node.
                for (Node neighbour : this.graph) {
                    if (!neighbour.isObstacle() && neighbour.getPosition().equals(neighbourPosition)) {
                        node.addNeighbour(neighbour);
                    }
                }
            }
        }
    }

    private void initializeRover(char character, Vector2D position) throws InvalidCommandArgumentException {
        // Verify that the rover has not already been parsed.
        if (this.rover != null) {
            throw new InvalidCommandArgumentException();
        }
        this.rover = new Rover(position);
        if (character == NodeType.ROVER_ON_DESTINATION_REPRESENTATION) {
            this.graph.add(new TerrainNode(NodeType.DESTINATION_REPRESENTATION,
                    NodeType.getFromRepresentation(NodeType.DESTINATION_REPRESENTATION),
                    position));
        } else {
            this.graph.add(new TerrainNode(NodeType.BACKGROUND_REPRESENTATION,
                    NodeType.getFromRepresentation(NodeType.BACKGROUND_REPRESENTATION),
                    position));
        }
    }

    private void initializeDestination(char character, Vector2D position) throws InvalidCommandArgumentException {
        // Verify that the destination has not already been parsed.
        if (hasDestination()) {
            throw new InvalidCommandArgumentException();
        }
        this.graph.add(new TerrainNode(character, NodeType.getFromRepresentation(character), position));
    }

    private boolean hasRover() {
        return this.rover != null;
    }

    private boolean hasDestination() {
        for (TerrainNode node : this.graph) {
            if (node.isDestination()) {
                return true;
            }
        }
        return false;
    }
}
