/*
 * Copyright (c) 2024, KASTEL. All rights reserved.
 */

package edu.kit.kastel.dotsandboxes.logic;

/**
 * This class initializes a game of {@link DotsAndBoxes} with specific starting conditions.
 *
 * @author Programmieren-Team
 */
public final class Initializer {

    private Initializer() {
        // utility class
    }

    /**
     * Initializes a new game.
     * @param mode the starting configuration of the game
     * @param length the side length of the game
     * @param players the players attending the game
     * @return a new game instance
     */
    public static DotsAndBoxes initialize(InitialisationMode mode, int length, Player... players) {
        DotsAndBoxes game = new DotsAndBoxes(length, players);
        boolean initialized =  switch (mode) {
            case AMERICANS -> initializeAmerican();
            case ICELANDIC -> initializeIcelandic(game, length);
            case SWEDISH -> initializeSwedish(game, length);
        };
        game.resetCurrentPlayer();
        return initialized ? game : null;
    }

    private static boolean initializeAmerican() {
        return true; // nothing to do here
    }

    private static boolean initializeIcelandic(DotsAndBoxes game, int length) {
        for (int i = 0; i < length; i++) {
            game.setBoxSide(0, i, Direction.LEFT);
            game.setBoxSide(i, length - 1, Direction.DOWN);
        }
        return true;
    }

    private static boolean initializeSwedish(DotsAndBoxes game, int length) {
        for (int i = 0; i < length; i++) {
            game.setBoxSide(0, i, Direction.LEFT);
            game.setBoxSide(i, length - 1, Direction.DOWN);
            game.setBoxSide(length - 1, i, Direction.RIGHT);
            game.setBoxSide(i, 0, Direction.UP);
        }
        return true;
    }
}
