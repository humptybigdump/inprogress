package edu.kit.kastel.commands;

import edu.kit.kastel.model.TerrainParser;
import edu.kit.kastel.model.NavigationSystem;

import java.util.regex.Pattern;

/**
 * This command retrieves a new visual of the surroundings from the rover.
 *
 *  @author uezxa
 *  @author udkdm
 */
public class NewTerrainCommand extends Command {
    private static final Pattern PATTERN = Pattern.compile("^new\\s+\\d+\\s+\\d+$");
    private static final int ARGUMENTS_WIDTH_INDEX = 1;
    private static final int ARGUMENTS_HEIGHT_INDEX = 2;

    /**
     * Constructs a new terrain command.
     *
     * @param handler          The command handler which is not used for this command
     * @param navigationSystem The navigation system to set the new map on it
     */
    public NewTerrainCommand(CommandHandler handler, NavigationSystem navigationSystem) {
        super(PATTERN, handler, navigationSystem);
    }

    @Override
    public void execute(String[] arguments) {
        int width = Integer.parseInt(arguments[ARGUMENTS_WIDTH_INDEX]);
        int height = Integer.parseInt(arguments[ARGUMENTS_HEIGHT_INDEX]);

        TerrainParser parser = new TerrainParser(width, height);

        for (int i = 0; i < height; i++) {
            String line = this.handler.getInput();
            try {
                parser.parseLine(line);
            } catch (InvalidCommandArgumentException exception) {
                System.err.println(exception.getMessage());
                this.handler.setRemainingTerrainLines(height - 1 - i);
                return;
            }
        }

        if (!parser.hasValidResult()) {
            System.err.println(ERROR_MESSAGE);
            return;
        }

        this.navigationSystem.setTerrain(parser.getMarsMap());
        this.navigationSystem.setRover(parser.getRover());
    }
}
