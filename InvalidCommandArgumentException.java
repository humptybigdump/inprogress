package edu.kit.kastel.commands;

/**
 * This exception is used to symbolize an error within the commands' execution
 * based on the provided arguments.
 *
 * @author uezxa
 * @author udkdm
 */
public class InvalidCommandArgumentException extends Exception {
    private static final String MESSAGE = "ERROR";

    /**
     * Constructs a new invalid command argument exception.
     *
     */
    public InvalidCommandArgumentException() {
        super(MESSAGE);
    }
}

