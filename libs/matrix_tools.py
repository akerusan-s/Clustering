def print_matrix(matrix):
    """ Procedures printing of 2-dim matrix """
    for i in matrix:
        for j in i:
            print(round(j, 3), end="\t")
        print()


def find_minimal_from_matrix(matrix):
    """ Return row, col, value of minimal element of matrix (value != 0)"""
    min_value = 10 ** 10
    min_row, min_col = 0, 0

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (matrix[i][j] < min_value) and (matrix[i][j] != 0):
                min_value = matrix[i][j]
                min_row = i
                min_col = j

    return min_row, min_col, min_value


def linear(matrix):
    """ Return linear list with values from 2-dim matrix """
    lin = []
    if matrix:
        for i in matrix:
            lin += i
        return lin
    return lin
