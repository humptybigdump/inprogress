/*
 * Copyright (c) 2024, KASTEL. All rights reserved.
 */

package edu.kit.kastel.dotsandboxes.logic;

/**
 * The available starting conditions.
 *
 * @author Programmieren-Team
 */
public enum InitialisationMode {

    /**
     * The default game mode. No modifications applied.
     */
    AMERICANS,
    /**
     * All lines on the most left and the most bottom sides are occupied.
     * Which player occupies them is not specified.
     * It's the regular first players turn after initialisation.
     */
    ICELANDIC,
    /**
     * All lines on the most outer edges in all directions are occupied.
     * Which player occupies them is not specified.
     * It's the regular first players turn after initialisation.
     */
    SWEDISH;
}
