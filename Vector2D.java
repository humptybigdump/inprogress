/*
 * Copyright (c) 2025, KASTEL. All rights reserved.
 */

package edu.kit.kastel.model;

import java.util.Objects;

/**
 * An immutable vector in 2D space.
 *
 * @author Programmieren-Team
 */
public class Vector2D {

    private static final String REPRESENTATION = "(%d,%d)";

    private final int x;
    private final int y;

    /**
     * Instantiates a new {@link Vector2D}.
     *
     * @param x the x value
     * @param y the y value
     */
    public Vector2D(int x, int y) {
        this.x = x;
        this.y = y;
    }

    /**
     * Returns the x value.
     *
     * @return the x value
     */
    public int getX() {
        return this.x;
    }

    /**
     * Returns the y value.
     *
     * @return the y value
     */
    public int getY() {
        return this.y;
    }

    /**
     * Adds the given vector to this vector component wise and returns the result.
     *
     * @param vector the vector to add
     * @return the resulting {@link Vector2D}
     */
    public Vector2D add(Vector2D vector) {
        return new Vector2D(this.x + vector.x, this.y + vector.y);
    }

    /**
     * Subtracts the given vector from this vector component wise and returns the
     * result.
     *
     * @param vector the vector to subtract
     * @return the resulting {@link Vector2D}
     */
    public Vector2D subtract(Vector2D vector) {
        return new Vector2D(this.x - vector.x, this.y - vector.y);
    }

    /**
     * Checks if this vector lies within the given boundaries.
     *
     * @param minX the minimum x value
     * @param minY the minimum y value
     * @param maxX the maximum x value
     * @param maxY the maximum y value
     * @return {@code true} iff this vector lies within the boundaries
     */
    public boolean liesWithinBoundaries(int minX, int minY, int maxX, int maxY) {
        return this.x >= minX && this.y >= minY && this.x <= maxX && this.y <= maxY;
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.x, this.y);
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

        Vector2D other = (Vector2D) obj;
        return this.x == other.x && this.y == other.y;
    }

    @Override
    public String toString() {
        return REPRESENTATION.formatted(this.x, this.y);
    }
}
