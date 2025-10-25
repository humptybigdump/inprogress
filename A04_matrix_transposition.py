def print_matrix(matrix):
    # Outer loop: iterate over the 'rows'
    for row in matrix:
        # Inner loop: iterate over the 'columns' of current 'row'
        for col in row:
            print(col, end='\t')
        print()


def transpose_matrix(matrix):
    transposed = []
    rows = len(matrix)
    cols = len(matrix[0])

    i = 0
    while i < cols:
        new_row = []
        j = 0
        while j < rows:
            new_row.append(matrix[j][i])
            j += 1
        transposed.append(new_row)
        i += 1

    return transposed

matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8 , 9],
          [10, 11, 12]]

print('original matrix:')
print_matrix(matrix)
print()

print('transposed matrix:')
print_matrix(transpose_matrix(matrix))

