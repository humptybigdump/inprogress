package edu.kit.kastel.util;

import edu.kit.kastel.Main;
import edu.kit.kastel.model.Direction;
import edu.kit.kastel.model.Node;
import edu.kit.kastel.model.Vector2D;

import java.util.LinkedList;
import java.util.Map;

/**
 * This class provides utility for finding paths.
 *
 * @author uezxa
 * @author udkdm
 */
public final class PathFinder {
    private PathFinder() {
        throw new AssertionError(Main.ERROR_UTILITY_CLASS);
    }

    /**
     * Finds the shortest path from the start node to the end node.
     *
     * @param start The start node
     * @param destination The destination node
     * @return The shortest path from the start node to the end note.
     */
    public static PathFinderResult findPath(Node start, Node destination) {
        // If destination is already reached return only the destination as a path.
        if (start.equals(destination)) {
            return new PathFinderResult(start.getPosition());
        }

        // Perform a BFS on the given start node.
        Map<Node, Node> parents = BreadthFirstSearch.bfs(start);
        // If the destination cannot be reached from the start, return an empty list.
        if (!parents.containsKey(destination)) {
            return new PathFinderResult();
        }

        return backTrack(start, destination, parents);
    }

    private static PathFinderResult backTrack(Node start, Node destination, Map<Node, Node> parents) {
        // Backtrack the path from the start to the destination.
        LinkedList<Vector2D> coordinates = new LinkedList<>();
        LinkedList<Direction> directions = new LinkedList<>();

        // Walk back the parent map from destination to start to extract the path.
        Node current = destination;
        coordinates.addFirst(current.getPosition());

        while (!current.equals(start)) {
            Node parent = parents.get(current);
            coordinates.addFirst(parent.getPosition());

            Direction direction = getDirection(parent, current);
            directions.addFirst(direction);
            current = parent;
        }
        return new PathFinderResult(coordinates, directions);
    }

    private static Direction getDirection(Node from, Node to) {
        Vector2D difference = to.getPosition().subtract(from.getPosition());
        return Direction.fromUnitVector(difference);
    }
}
