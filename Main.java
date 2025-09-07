package task1;

public class Main {
    public static void main(String[] args) {
        // Initialize a new Grid
        Grid grid = new Grid(Cell.startCell(), Cell.goalCell());
        // Print the grid to the user
        System.out.println(grid);

        // Using BFS find the shortest path from start to goal
        GridUtility.bfs(grid);
        System.out.println(grid);
    }
}