package edu.kit.kastel.model;

/**
 * This class represents the Mars rover that can move on the terrain.
 *
 * @author uezxa
 * @author udkdm
 */
public class Rover {

    /**
     * Represents a rover on the terrain.
     */
    public static final char REPRESENTATION = 'R';
    private Vector2D position;

    /**
     * Constructs a new rover.
     *
     * @param position The initial position of the rover
     */
    public Rover(Vector2D position) {
        this.position = position;
    }

    /**
     * Gets the position of the rover.
     *
     * @return The position of the rover
     */
    public Vector2D getPosition() {
        return position;
    }

    /**
     * Moves the rover one step to the given direction.
     *
     * @param direction The given direction
     *
     */
    public void move(Direction direction) {
        this.position = this.position.add(direction.getUnitVector());
    }

    @Override
    public String toString() {
        return String.valueOf(REPRESENTATION);
    }
}
