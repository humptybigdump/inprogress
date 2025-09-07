package edu.kit.kastel.commands;

import edu.kit.kastel.model.Direction;
import edu.kit.kastel.model.NavigationSystem;
import edu.kit.kastel.model.Node;
import edu.kit.kastel.model.Rover;
import edu.kit.kastel.model.Terrain;

import java.util.regex.Pattern;

/**
 * This command moves the rover on the terrain in the specified direction.
 * The user can specify a direction (e.g., "up", "down", "left", "right") and an optional step count.
 * If no step count is provided, the rover moves a single step in the given direction.
 *
 * @author uezxa
 * @author udkdm
 */
public class MoveCommand extends Command {
    private static final Pattern PATTERN = Pattern.compile("^(up|down|left|right)(\\s+\\d+)?$");
    private static final int ARGUMENTS_MOVE_COUNT_INDEX = 1;
    private static final int DEFAULT_MOVE_COUNT = 1;

    /**
     * Constructs a new {@code MoveCommand}.
     *
     * @param handler The {@link CommandHandler}, which is not used for this command
     * @param navigationSystem The {@link NavigationSystem} used to move the rover
     */
    public MoveCommand(CommandHandler handler, NavigationSystem navigationSystem) {
        super(PATTERN, handler, navigationSystem);
    }

    @Override
    public void execute(String[] arguments) {
        try {
            this.navigationSystem.requireOperativeSystem();
        } catch (InvalidCommandArgumentException exception) {
            System.err.println(exception.getMessage());
            return;
        }

        Direction direction = Direction.fromString(arguments[ARGUMENTS_COMMAND_INDEX]);
        Terrain terrain = this.navigationSystem.getTerrain();
        Rover rover = this.navigationSystem.getRover();

        // If the user wants to move multiple steps at once override the amount of steps.
        int amount = arguments.length > ARGUMENTS_DEFAULT_LENGTH
                ? Integer.parseInt(arguments[ARGUMENTS_MOVE_COUNT_INDEX])
                : DEFAULT_MOVE_COUNT;

        for (int i = 0; i < amount; i++) {
            Node node = terrain.getNodeByPosition(rover.getPosition().add(direction.getUnitVector()));
            if (node != null && !node.isObstacle()) {
                rover.move(direction);
            }
        }
    }
}
