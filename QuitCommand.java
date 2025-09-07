package edu.kit.kastel.commands;

import edu.kit.kastel.model.NavigationSystem;

import java.util.regex.Pattern;

/**
 * A command that quits the application when executed.
 * This command calls the {@code quit()} method of the provided {@link CommandHandler}.
 *
 * @author uezxa
 * @author udkdm
 */
public class QuitCommand extends Command {
    private static final Pattern PATTERN = Pattern.compile("^quit$");

    /**
     * Constructs a new {@code QuitCommand}.
     *
     * @param handler The {@link CommandHandler} responsible for managing application commands
     * @param navigationSystem The {@link NavigationSystem}, which is not used in this command
     */
    public QuitCommand(CommandHandler handler, NavigationSystem navigationSystem) {
        super(PATTERN, handler, navigationSystem);
    }

    @Override
    public void execute(String[] arguments) {
        this.handler.quit();
    }
}
