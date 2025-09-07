package edu.kit.kastel.model;

import edu.kit.kastel.commands.InvalidCommandArgumentException;
import edu.kit.kastel.util.PathFinder;
import edu.kit.kastel.util.PathFinderResult;

import java.util.List;
import java.util.StringJoiner;

/**
 * Heart of the application. Manages the rovers movements on the Mars map.
 *
 * @author uezxa
 * @author udkdm
 */
public class NavigationSystem {
    private static final char PATH_REPRESENTATION = '.';

    private Terrain terrain;
    private Rover rover;

    /**
     * Constructs a new navigation system.
     */
    public NavigationSystem() {
        this.terrain = null;
        this.rover = null;
    }

    /**
     * Gets the Mars map of the navigation system.
     *
     * @return The Mars map of the navigation system
     */
    public Terrain getTerrain() {
        return terrain;
    }

    /**
     * Gets the rover of the navigation system.
     *
     * @return The rover of the navigation system
     */
    public Rover getRover() {
        return rover;
    }

    /**
     * Sets the Mars map.
     *
     * @param terrain The new Mars map
     */
    public void setTerrain(Terrain terrain) {
        this.terrain = terrain;
    }

    /**
     * Sets the rover.
     *
     * @param rover the new rover
     */
    public void setRover(Rover rover) {
        this.rover = rover;
    }

    /**
     * Returns a debug of the Mars map also showing a path if provided.
     *
     * @param path The path that can be shown
     * @return The debug of the Mars map
     * @throws InvalidCommandArgumentException If the system is not operative yet
     */
    public String debug(List<Vector2D> path) throws InvalidCommandArgumentException {
        requireOperativeSystem();

        // Get the terrain as a char array.
        char[][] terrain = this.terrain.asArray();

        // If there is a path it should be displayed on the map.
        if (!path.isEmpty()) {
            // Replace all nodes that are on the path with a dot.
            for (Vector2D position : path) {
                Node node = this.terrain.getNodeByPosition(position);
                if (node.getRepresentation() != Rover.REPRESENTATION && node.getRepresentation() != NodeType.DESTINATION_REPRESENTATION) {
                    terrain[node.getPosition().getY()][node.getPosition().getX()] = PATH_REPRESENTATION;
                }
            }
        }

        // Place the rover on the terrain.
        placeRover(terrain);

        StringJoiner joiner = new StringJoiner(System.lineSeparator());
        for (char[] line : terrain) {
            joiner.add(String.valueOf(line));
        }
        return joiner.toString();
    }

    /**
     * Finds the path from the rover to the destination.
     * @return The {@code PathFinderResult} of the search
     * @throws InvalidCommandArgumentException If the system is not operative yet
     */
    public PathFinderResult findPathToDestination() throws InvalidCommandArgumentException {
        requireOperativeSystem();

        // Extract valuable positions on the terrain.
        Node start = this.terrain.getNodeByPosition(rover.getPosition());
        Node destination = this.terrain.getDestination();

        // Find the shortest path from the rover to the destination.
        return PathFinder.findPath(start, destination);
    }

    /**
     * Forces the system to be initialized with a rover and a terrain.
     *
     * @throws InvalidCommandArgumentException If either rover or terrain are missing
     */
    public void requireOperativeSystem() throws InvalidCommandArgumentException {
        if (!isOperativeSystem()) {
            throw new InvalidCommandArgumentException();
        }
    }

    private boolean isOperativeSystem() {
        return terrain != null && rover != null;
    }

    private void placeRover(char[][] terrain) {
        int x = this.rover.getPosition().getX();
        int y = this.rover.getPosition().getY();
        if (terrain[y][x] == NodeType.DESTINATION_REPRESENTATION) {
            terrain[y][x] = NodeType.ROVER_ON_DESTINATION_REPRESENTATION;
        } else {
            terrain[y][x] = Rover.REPRESENTATION;
        }
    }


}
