/*
 * Copyright (c) 2024, KASTEL. All rights reserved.
 */

package edu.kit.kastel.dotsandboxes.logic;

/**
 * A player of {@link DotsAndBoxes}.
 *
 * @author Programmieren-Team
 */
public class Player {

    private final String name;
    private int score;

    /**
     * Creates a new player.
     * @param name the name of the player
     */
    public Player(String name) {
        this.name = name;
    }

    /**
     * Increments the score by one.
     */
    void incrementScore() {
        this.score++;
    }

    /**
     * Returns the current score.
     * @return the current score
     */
    public int getScore() {
        return score;
    }

    @Override
    public String toString() {
        return name;
    }
}
