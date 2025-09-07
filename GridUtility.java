package task1;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public final class GridUtility {
    private GridUtility() {
        throw new AssertionError("Utility class cannot be instantiated.");
    }

    public static void bfs(Grid grid) {
        Queue<Cell> queue = new LinkedList<>();

        // Add the starting cell to the Queue
        queue.add(grid.getStart());

        // Continue while we are still searching for the goal
        while (!queue.isEmpty()) {
            Cell current = queue.poll();
            // Skip already visited cells
            if (current.isVisited()) {
                continue;
            }

            // Mark the current cell as visited
            current.visit();

            // Check if the goal is reached
            if (current.isGoal()) {
                return;
            }

            // Add valid neighbors to the queue
            for (Cell neighbour : getNeighbours(grid, current)) {
                if (!neighbour.isVisited()) {
                    queue.add(neighbour);
                }
            }

            // Print the grid state after each step
            System.out.println(grid);
        }
        // If the goal was not found
        System.out.println("Goal not reachable.");
    }


    private static List<Cell> getNeighbours(Grid grid, Cell cell) {
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