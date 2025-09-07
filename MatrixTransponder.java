package task1;

public final class MatrixTransponder {
    private static final String SEPARATOR = " ";

    private MatrixTransponder() {
        throw new IllegalArgumentException("Cannot instantiate utility class.");
    }

    public static void main(String[] args) {
        int[][] matrix = {{0, 0, 0}, {1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        System.out.println("Ursprüngliche Matrix:");
        printMatrix(matrix);

        System.out.println(System.lineSeparator() + "Transponierte Matrix:");
        printMatrix(transpond(matrix));
    }

    private static int[][] transpond(int[][] matrix) {
        int[][] transpond = new int[matrix[0].length][matrix.length];
        for (int i = 0; i < transpond.length; i++) {
            for (int j = 0; j < transpond[i].length; j++) {
                transpond[i][j] = matrix[j][i];
            }
        }
        return transpond;
    }

    private static void printMatrix(int[][] matrix) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                builder.append(matrix[i][j]);
                if (j < matrix[i].length - 1) {
                    builder.append(SEPARATOR);
                }
            }
            builder.append(System.lineSeparator());
        }
        System.out.println(builder);
    }
}