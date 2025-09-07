package edu.kit.kastel;

public class Application {
    public static void main(String[] args) {
        CommandHandler handler = new CommandHandler(new HighscoreTable());
        handler.listen();
    }
}
