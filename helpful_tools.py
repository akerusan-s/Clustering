def print_matrix(matrix):
    """ Procedures printing of 2-dim matrix """
    for i in matrix:
        for j in i:
            print(round(j, 3), end="\t")
        print()


def find_minimal_from_matrix(matrix):
    """ Returns row, col, value of minimal element of matrix """
    min_value = min([min([j if j != 0 else 10**10 for j in i]) for i in matrix])

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == min_value:
                return i, j, min_value
