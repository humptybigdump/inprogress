package edu.kit.kastel;

import java.util.Arrays;
import java.util.Scanner;

public class CommandHandler {
    private final HighscoreTable scores;
    private boolean isRunning;

    public CommandHandler(HighscoreTable scores) {
        this.isRunning = true;
        this.scores = scores;
    }

    public void listen() {
        try (Scanner scanner = new Scanner(System.in)) {
            while (scanner.hasNextLine() && isRunning) {
                String currentLine = scanner.nextLine();
                String[] input = currentLine.split(" ");

                String commandName = input[0];
                String[] userArguments = Arrays.copyOfRange(input, 1, input.length);
                System.out.println(handleCommand(commandName, userArguments));
            }
        }
    }

    public String handleCommand(String commandName, String[] commandArguments) {
        switch (commandName) {
            case "score" -> {
                scores.addScore(commandArguments[0], Integer.parseInt(commandArguments[1]));
                return "Player %s has been registered".formatted(commandArguments[0]);
            }
            case "remove-score" -> {
                scores.removePlayer(commandArguments[0]);
                return "Player %s has been unregistered".formatted(commandArguments[0]);
            }
            case "top-scores" -> {
                return scores.getTopScores(Integer.parseInt(commandArguments[0])).toString();
            }
            case "see-list" -> {
                return scores.toString();
            }
            case "player-score" -> {
                return String.valueOf(scores.getPlayerScore(commandArguments[0]).getScore());
            }
            case "reset-scores" -> {
                scores.resetScores();
                return "Score list has been reset!";
            }
            case "get-scores-above" -> {
                return scores.getScoresAbove(Integer.parseInt(commandArguments[0])).toString();
            }
            case "quit" -> {
                isRunning = false;
                return "";
            }
            default -> {
                return "Unknown command %s!".formatted(commandName);
            }
        }
    }
}
