package task1;

import java.util.Random;

public class Grid {



    // TODO Use those in BFS Class
    private static final String VISITED = "🟦";



    private static final int GRID_SIZE = 10;
    private final Random random = new Random();
    private final Cell[][] grid = new Cell[GRID_SIZE][GRID_SIZE];
    private final Cell start;
    private final Cell goal;

    public Grid(Cell start, Cell goal) {
        // Set the start and goal
        this.start = start;
        this.goal = goal;

        // Initialize Map
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                grid[i][j] = Cell.emptyCell();
            }
        }

        // Randomly place obstacles and the start and goal on the Map
        placeObstacles();
        placeStartAndGoal();
    }

    public Cell getStart() {
        return start;
    }

    public int getSize() {
        return GRID_SIZE;
    }

    public Cell getCell(int x, int y) {
        return grid[x][y];
    }

    public int[] getCellPosition(Cell cell) {
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j] == cell) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[]{-1, -1};
    }

    private void placeObstacles() {
        // Fill 20% of the map with obstacles
        int obstacleCount = (GRID_SIZE * GRID_SIZE) / 5;

        for (int i = 0; i < obstacleCount; i++) {
            placeRandomly(Cell.obstacleCell());
        }
    }

    private void placeStartAndGoal() {
        placeRandomly(start);
        placeRandomly(goal);
    }

    private void placeRandomly(Cell cell) {
        int x, y;
        do {
            x = random.nextInt(GRID_SIZE);
            y = random.nextInt(GRID_SIZE);
        } while (!grid[x][y].isEmpty());
        grid[x][y] = cell;
    }

    @Override
    public String toString() {
        StringBuilder stringBuilder = new StringBuilder();
        for (Cell[] row : grid) {
            for (Cell cell : row) {
                stringBuilder.append(cell).append(" ");
            }
            stringBuilder.append(System.lineSeparator());
        }
        return stringBuilder.toString();
    }
}
