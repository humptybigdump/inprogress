package edu.kit.kastel;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.StringJoiner;

public class HighscoreTable {
    private static final String OUTPUT_FORMAT = "Player %s has scored %d points!";

    private final List<PlayerScore> playerScores;

    public HighscoreTable() {
        playerScores = new ArrayList<>();
    }

    public void addScore(String playerName, int score) {
        for (PlayerScore playerScore : playerScores) {
            if (playerScore.getPlayerName().equals(playerName)) {
                playerScore.setScore(score);
                return;
            }
        }
        playerScores.add(new PlayerScore(playerName, score));
    }

    public boolean removePlayer(String playerName) {
        for (PlayerScore playerScore : playerScores) {
            if (playerScore.getPlayerName().equals(playerName)) {
                return playerScores.remove(playerScore);
            }
        }
        return false;
    }

    public List<PlayerScore> getTopScores(int n) {
        Collections.sort(playerScores);
        playerScores.reversed();
        return playerScores.subList(0, Math.min(n, playerScores.size()));
    }

    public List<PlayerScore> getScoresAbove(int minScore) {
        List<PlayerScore> scores = new ArrayList<>();
        for (PlayerScore playerScore : playerScores) {
            if (playerScore.getScore() >= minScore) {
                scores.add(playerScore);
            }
        }
        return scores;
    }

    public PlayerScore getPlayerScore(String playerName) {
        for (PlayerScore playerScore : playerScores) {
            if (playerScore.getPlayerName().equals(playerName)) {
                return playerScore;
            }
        }
        return null;
    }

    public void resetScores() {
        playerScores.clear();
    }

    @Override
    public String toString() {
        StringJoiner lines = new StringJoiner(System.lineSeparator());
        for (PlayerScore playerScore : playerScores) {
            lines.add(String.format(OUTPUT_FORMAT, playerScore.getPlayerName(), playerScore.getScore()));
        }
        return lines.toString();
    }
}
