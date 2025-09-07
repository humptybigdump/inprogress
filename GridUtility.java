package task1;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public final class GridUtility {
    private GridUtility() {
        throw new AssertionError("Utility class cannot be instantiated.");
    }

    public static void bfs(task1.Grid grid) {
        //TODO implement Breadth-First-Search
    }


    private static Lsist<Cell> getNeighbours(Grid grid, Cell cell) {
        List<Cell> neighbours = new ArrayList<>();
        int[] position = grid.getCellPosition(cell);
        int x = position[0];
        int y = position[1];

        int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        for (int[] dir : directions) {
            int newX = x + dir[0];
            int newY = y + dir[1];

            if (newX >= 0 && newY >= 0 && newX < grid.getSize() && newY < grid.getSize()) {
                Cell neighbour = grid.getCell(newX, newY);
                // Add neighbor if it is unvisited and empty
                if (!neighbour.isObstacle()) {
                    neighbours.add(neighbour);
                }
            }
        }
        return neighbours;
    }
}