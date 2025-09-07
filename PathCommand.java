package edu.kit.kastel.commands;

import edu.kit.kastel.model.Direction;
import edu.kit.kastel.model.NavigationSystem;
import edu.kit.kastel.util.PathFinderResult;

import java.util.List;
import java.util.regex.Pattern;

/**
 * This command explains the path to the destination to the rover.
 *
 *  @author uezxa
 *  @author udkdm
 */
public class PathCommand extends Command {
    private static final Pattern PATTERN = Pattern.compile("^path$");
    private static final String PATH_MESSAGE = "PATH %d";
    private static final String NO_PATH_FOUND = "FAIL";

    /**
     * Constructs a new path command.
     *
     * @param handler The command handler which is not used for this command
     * @param navigationSystem The navigation system to set the new map on it
     */
    public PathCommand(CommandHandler handler, NavigationSystem navigationSystem) {
        super(PATTERN, handler, navigationSystem);
    }

    @Override
    public void execute(String[] arguments) {
        PathFinderResult result;
        try {
            result = this.navigationSystem.findPathToDestination();
        } catch (InvalidCommandArgumentException exception) {
            System.err.println(exception.getMessage());
            return;
        }

        if (result.isEmpty()) {
            System.out.println(NO_PATH_FOUND);
            return;
        }

        List<Direction> directions = result.getDirections();

        System.out.println(PATH_MESSAGE.formatted(directions.size()));
        for (Direction direction : directions) {
            System.out.println(direction);
        }
    }
}
