

# n×n 크기의 2차원 배열 생성
def create_matrix(n):
    matrix = []

    for i in range(n):
        row = [0.0] * n
        matrix.append(row)

    return matrix


# 지정한 행과 열의 값 읽기
def get_value(matrix, row, col):
    return matrix[row][col]


# 지정한 행과 열의 값 수정하기
def set_value(matrix, row, col, value):
    matrix[row][col] = value


def input_matrix():
    matrix = []

    for i in range(3):
        while True:
            text = input(f"{i + 1}행 입력 (숫자 3개): ")

            try:
                row = list(map(float, text.split()))

                if len(row) != 3:
                    print("오류: 숫자를 정확히 3개 입력하세요.")
                    continue

                matrix.append(row)
                break

            except ValueError:
                print("오류: 숫자만 입력하세요.")

    return matrix