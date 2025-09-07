package edu.kit.kastel;

public class PlayerScore implements Comparable<PlayerScore> {
    private static final String REPRESENTATION = "(%s:%d)";

    private final String playerName;
    private int score;

    public PlayerScore(String playerName, int score) {
        this.playerName = playerName;
        this.score = score;
    }

    public String getPlayerName() {
        return playerName;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    @Override
    public int compareTo(PlayerScore playerScore) {
        return Integer.compare(score, playerScore.getScore());
    }

    @Override
    public String toString() {
        return REPRESENTATION.formatted(playerName, score);
    }
}
