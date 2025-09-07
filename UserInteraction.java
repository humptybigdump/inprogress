/*
 * Copyright (c) 2024, KASTEL. All rights reserved.
 */

package edu.kit.kastel.dotsandboxes.view;

import edu.kit.kastel.dotsandboxes.logic.Direction;
import edu.kit.kastel.dotsandboxes.logic.DotsAndBoxes;
import edu.kit.kastel.dotsandboxes.logic.Box;

import java.util.Scanner;
import java.util.StringJoiner;

/**
 * The interactive user interface capable of managing a {@link DotsAndBoxes}.
 *
 * @author Programmieren-Team
 */
public class UserInteraction {

    private static final String TERMINATION_INPUT = "quit";
    private static final int INPUT_SEQUENCE_INDEX_COLUMN = 0;
    private static final int INPUT_SEQUENCE_INDEX_ROW = 1;
    private static final char BASE_VALUE_COLUMNS = 'a';
    private static final char BASE_VALUE_ROWS = '1';
    private static final int EXPECTED_NUMBER_OF_ARGUMENTS = 2;
    private static final String ARGUMENT_SEPARATOR = " ";
    private static final int ARGUMENT_INDEX_POSITION = 0;
    private static final int POSITION_LENGTH = 2;
    private static final int ARGUMENT_INDEX_DIRECTION = 1;
    private static final String EXTRA_INFO_WINNER_FORMAT = "Player %s wins!%n";
    private static final String EXTRA_INFO_PLAYERS_TURN_FORMAT = "Player %s:%n";
    private static final String PRINT_COLUMN_SPREAD = " ";
    private static final String PRINT_SEPARATOR_INDICATOR_ROW = PRINT_COLUMN_SPREAD + " " + PRINT_COLUMN_SPREAD;
    private static final String PRINT_SEPARATOR_UPPER_TILE_ROW = PRINT_COLUMN_SPREAD + "+" + PRINT_COLUMN_SPREAD;
    private static final String PRINT_EMPTY_BOX_OWNER = " ";
    private static final String PRINT_EMPTY_BOX_EDGE = " ";
    private static final String PRINT_HORIZONTAL_BOX_EDGE = "-";
    private static final String PRINT_VERTICAL_BOX_EDGE = "|";
    private final DotsAndBoxes game;

    /**
     * Creates a new instance.
     * @param game the game to be managed by this instance
     */
    public UserInteraction(DotsAndBoxes game) {
        this.game = game;
    }

    /**
     * Initiates the interaction with the user.
     */
    public void start() {
        printExtra(true);
        try (Scanner scan = new Scanner(System.in)) {
            while (!game.isFinished()) {
                String input = scan.nextLine();
                if (input.equals(TERMINATION_INPUT)) {
                    break;
                }

                printExtra(processInput(input));
            }
        }
    }

    private boolean processInput(String input) {
        String[] splitArguments = input.split(ARGUMENT_SEPARATOR);
        if (splitArguments.length != EXPECTED_NUMBER_OF_ARGUMENTS 
                || splitArguments[ARGUMENT_INDEX_POSITION].length() != POSITION_LENGTH) {
            return false;
        }
        
        int column = input.charAt(INPUT_SEQUENCE_INDEX_COLUMN) - BASE_VALUE_COLUMNS;
        int row = input.charAt(INPUT_SEQUENCE_INDEX_ROW) - BASE_VALUE_ROWS;
        Direction direction = Direction.fromRepresentation(splitArguments[ARGUMENT_INDEX_DIRECTION]);
        
        return direction != null && game.setBoxSide(column, row, direction);
    }

    private void printExtra(boolean printGameState) {
        if (printGameState) {
            System.out.println(currentGameState());
        }
        System.out.printf((game.isFinished() ? EXTRA_INFO_WINNER_FORMAT : EXTRA_INFO_PLAYERS_TURN_FORMAT),
                game.isFinished() ? game.getWinner() : game.getCurrentPlayer());
    }

    private String currentGameState() {
        StringJoiner rowJoiner = new StringJoiner(System.lineSeparator());

        rowJoiner.add(getColumnIndicatorRow());
        addUpperAndMiddleTileRows(rowJoiner);
        rowJoiner.add(getLowerRow());

        return rowJoiner.toString();
    }

    private String getColumnIndicatorRow() {
        StringJoiner columnIndicatorRowBuilder = new StringJoiner(PRINT_SEPARATOR_INDICATOR_ROW, PRINT_SEPARATOR_INDICATOR_ROW,
                PRINT_SEPARATOR_INDICATOR_ROW.substring(0, PRINT_SEPARATOR_INDICATOR_ROW.length() - 1));
        for (int i = 0; i < game.getLength(); i++) {
            columnIndicatorRowBuilder.add(String.valueOf((char) (BASE_VALUE_COLUMNS + i)));
        }
        return columnIndicatorRowBuilder.toString().stripTrailing();
    }

    private void addUpperAndMiddleTileRows(StringJoiner rowJoiner) {
        for (int tileRow = 0; tileRow < game.getLength(); tileRow++) {
            StringJoiner upperRow = new StringJoiner(PRINT_SEPARATOR_UPPER_TILE_ROW, PRINT_SEPARATOR_UPPER_TILE_ROW,
                    PRINT_SEPARATOR_UPPER_TILE_ROW);
            StringJoiner middleRow = new StringJoiner(PRINT_COLUMN_SPREAD, String.valueOf(tileRow + 1), "");
            for (int tileColumn = 0; tileColumn < game.getLength(); tileColumn++) {
                Box box = game.get(tileColumn, tileRow);
                upperRow.add(box.isOccupied(Direction.UP) ? PRINT_HORIZONTAL_BOX_EDGE : PRINT_EMPTY_BOX_EDGE);

                middleRow.add(box.isOccupied(Direction.LEFT) ? PRINT_VERTICAL_BOX_EDGE : PRINT_EMPTY_BOX_EDGE);
                middleRow.add(box.isClosed() ? box.getOwner().toString() : PRINT_EMPTY_BOX_OWNER);
            }
            middleRow.add(game.get(game.getLength() - 1, tileRow).isOccupied(Direction.RIGHT)
                    ? PRINT_VERTICAL_BOX_EDGE
                    : PRINT_EMPTY_BOX_EDGE);

            rowJoiner.add(upperRow.toString().stripTrailing());
            rowJoiner.add(middleRow.toString().stripTrailing());
        }
    }

    private String getLowerRow() {
        StringJoiner lowerRow = new StringJoiner(PRINT_SEPARATOR_UPPER_TILE_ROW, PRINT_SEPARATOR_UPPER_TILE_ROW,
                PRINT_SEPARATOR_UPPER_TILE_ROW);
        for (int tileColumn = 0; tileColumn < game.getLength(); tileColumn++) {
            lowerRow.add(game.get(tileColumn, game.getLength() - 1).isOccupied(Direction.DOWN)
                    ? PRINT_HORIZONTAL_BOX_EDGE
                    : PRINT_EMPTY_BOX_EDGE);
        }
        return lowerRow.toString().stripTrailing();
    }
}
