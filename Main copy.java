package edu.kit.kastel;

import edu.kit.kastel.commands.CommandHandler;
import edu.kit.kastel.model.NavigationSystem;

/**
 * Main entry point to the application.
 *
 * @author uezxa
 * @author udkdm
 */
public final class Main {
    /**
     * Error message when a utility class is being instantiated.
     */
    public static final String ERROR_UTILITY_CLASS = "Utility class cannot be instantiated.";

    private Main() {
        throw new AssertionError(ERROR_UTILITY_CLASS);
    }

    /**
     * Main method of the application.
     *
     * @param args The command-line arguments (ignored)
     */
    public static void main(String[] args) {
        CommandHandler handler = new CommandHandler(new NavigationSystem());
        handler.handleInput();
    }
}
