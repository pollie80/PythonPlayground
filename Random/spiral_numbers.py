def spiral_matrix(size):
    new_matrix = [[0] for _ in range(size)]

    for i in range()

    return new_matrix


def print_spiral_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            print("{:2d}".format(matrix[i][j]), end=" ")
        print()


if __name__ == "__main__":
    n = int(input("Enter the size of the matrix(): "))
    matrix = spiral_matrix(n)
    print("Spiral Matrix:")
    print_spiral_matrix(matrix)
