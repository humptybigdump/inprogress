package edu.kit.kastel.util;

import edu.kit.kastel.model.Direction;
import edu.kit.kastel.model.Vector2D;

import java.util.Collections;
import java.util.List;

/**
 * Represents the result of the PathFinder.
 *
 * @author uezxa
 * @author udkdm
 */
public class PathFinderResult {
    private final List<Vector2D> coordinates;
    private final List<Direction> directions;

    /**
     * Constructs a new and empty result without a path.
     */
    public PathFinderResult() {
        this.coordinates = List.of();
        this.directions = List.of();
    }

    /**
     * Constructs a new result with only one element. This element will be the start and destination of the path.
     *
     * @param position The only position element
     */
    public PathFinderResult(Vector2D position) {
        this.coordinates = List.of(position);
        this.directions = List.of();
    }

    /**
     * Constructs a new result.
     *
     * @param coordinates The coordinates of the path
     * @param directions The directions needed to get from start to destination
     */
    public PathFinderResult(List<Vector2D> coordinates, List<Direction> directions) {
        this.coordinates = Collections.unmodifiableList(coordinates);
        this.directions = Collections.unmodifiableList(directions);
    }

    /**
     * Returns an unmodifiable list of the coordinates.
     *
     * @return the coordinates
     */
    public List<Vector2D> getCoordinates() {
        return this.coordinates;
    }

    /**
     * Returns an unmodifiable list of directions.
     *
     * @return the directions
     */
    public List<Direction> getDirections() {
        return this.directions;
    }

    /**
     * Returns True if this result does not contain a path.
     *
     * @return True if this result does not contain a path
     */
    public boolean isEmpty() {
        return this.coordinates.isEmpty();
    }
}
