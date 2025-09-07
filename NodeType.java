package edu.kit.kastel.model;


import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Represents different types of nodes on a graph.
 *
 * @author uezxa
 * @author udkdm
 */
public enum NodeType {
    /**
     * An empty node where the rover can safely drive on.
     */
    EMPTY,

    /**
     * Obstacles that the rover needs to avoid.
     */
    OBSTACLE,

    /**
     * The destination that the rover wants to reach.
     */
    DESTINATION;

    /**
     * Represents the rover.
     */
    static final char ROVER_REPRESENTATION = 'R';

    /**
     * Represents a destination node.
     */
    static final char DESTINATION_REPRESENTATION = 'x';

    /**
     * Represents the rover standing on top of the destination.
     */
    static final char ROVER_ON_DESTINATION_REPRESENTATION = 'X';

    /**
     * Represents the background of the terrain.
     */
    static final char BACKGROUND_REPRESENTATION = ' ';

    /**
     * Represents all obstacle representations on the terrain.
     */
    static final List<Character> OBSTACLES_REPRESENTATION = Arrays.asList('|', '_', '/', '\\', '*');

    /**
     * Represents all legal representation on the terrain.
     */
    static final List<Character> LEGAL_CHARACTERS = new ArrayList<>();

    static {
        LEGAL_CHARACTERS.add(ROVER_REPRESENTATION);
        LEGAL_CHARACTERS.add(DESTINATION_REPRESENTATION);
        LEGAL_CHARACTERS.add(ROVER_ON_DESTINATION_REPRESENTATION);
        LEGAL_CHARACTERS.add(BACKGROUND_REPRESENTATION);
        LEGAL_CHARACTERS.addAll(OBSTACLES_REPRESENTATION);
    }

    /**
     * Gets the corresponding node type by its representation.
     *
     * @param character The representation of the node
     * @return The corresponding node type
     */
    public static NodeType getFromRepresentation(char character) {
        if (character == BACKGROUND_REPRESENTATION) {
            return EMPTY;
        } else if (character == DESTINATION_REPRESENTATION) {
            return DESTINATION;
        } else if (OBSTACLES_REPRESENTATION.contains(character)) {
            return OBSTACLE;
        } else {
            return null;
        }
    }
}
