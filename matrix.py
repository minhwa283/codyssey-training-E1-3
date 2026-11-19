
# ============================================================
# 파일명: matrix.py
# 설명: Mini NPU에서 사용하는 2차원 배열을 관리하는 파일
#
# 주요 기능
# 1. n×n 크기의 2차원 리스트 생성
# 2. 특정 행과 열에 있는 값 읽기
# 3. 특정 행과 열에 있는 값 수정
# 4. 배열 크기와 숫자 자료형 검사
# 5. 사용자에게 3×3 배열 입력받기
# ============================================================


# [함수] create_matrix(n)
# 기능: n행 × n열의 정사각형 배열을 생성한다.
# 매개변수 n: 행과 열의 개수
# 반환값: 0.0으로 채워진 2차원 리스트
def create_matrix(n):
    # 이 matrix는 create_matrix() 함수 안에서 사용하는 지역변수
    matrix = []

    # range(n): 0부터 n-1까지 반복하므로 총 n번 실행
    for i in range(n):

        # [0.0] * n: 0.0이 n개 들어 있는 리스트 생성
        # 예: n=3이면 [0.0, 0.0, 0.0]
        row = [0.0] * n

        # append(): 리스트의 맨 뒤에 요소 하나 추가
        # 여기서는 row 리스트 전체를 matrix에 추가
        matrix.append(row)

    # 완성된 2차원 리스트를 호출한 곳으로 반환
    return matrix


# [함수] get_value(matrix, row, col)
# 기능: 2차원 리스트의 특정 위치에 저장된 값을 읽는다.
# matrix: 전달받은 2차원 리스트 (매개변수)
# row: 행 번호 / col: 열 번호 (모두 0부터 시작)
def get_value(matrix, row, col):
    # matrix[행][열]
    # 예: matrix[1][1]은 두 번째 행의 두 번째 값
    return matrix[row][col]


# [함수] set_value(matrix, row, col, value)
# 기능: 2차원 리스트의 특정 위치에 새로운 값을 저장한다.
# value: 새로 저장할 숫자
def set_value(matrix, row, col, value):
    # 전달받은 리스트 자체를 수정하므로 별도의 return은 필요 없음
    matrix[row][col] = value


# [함수] validate_matrix(matrix, n)
# 기능: 배열이 n×n 구조이고 모든 값이 숫자인지 검사한다.
# 반환값: 정상 True / 비정상 False
def validate_matrix(matrix, n):

    # isinstance(값, 자료형): 지정한 자료형인지 검사
    # not: 검사 결과를 반대로 바꿈
    if not isinstance(matrix, list):
        return False

    # 바깥 리스트의 요소 개수 = 행 개수
    if len(matrix) != n:
        return False

    # 각 행을 하나씩 꺼내서 검사
    for row in matrix:

        # 각 행도 리스트여야 함
        if not isinstance(row, list):
            return False

        # 각 행에 들어 있는 값의 개수 = 열 개수
        if len(row) != n:
            return False

        # 행에 들어 있는 숫자를 하나씩 검사
        for value in row:

            # type(value): 값의 자료형 확인
            # int: 정수 / float: 실수
            # not in: 지정한 자료형 목록에 포함되지 않는지 확인
            if type(value) not in (int, float):
                return False

    # 모든 검사를 통과하면 정상
    return True


# [함수] input_matrix(name)
# 기능: 사용자에게 3×3 배열을 입력받는다.
# name: 화면에 표시할 배열 이름 (기본값은 "배열")
# 반환값: 사용자가 입력한 3×3 리스트
def input_matrix(name="배열"):
    matrix = []

    print(f"\n{name} (3×3)을 입력하세요.")
    print("숫자 3개를 공백으로 구분하세요.")

    # 3행을 입력받기 위해 총 3번 반복
    for i in range(3):

        # 올바른 값이 들어올 때까지 반복
        while True:

            # f문자열: { } 안에 변수나 계산 결과를 넣을 수 있음
            # i+1: 사용자에게 행 번호를 1부터 보여주기 위함
            text = input(f"{i + 1}행 입력: ")

            # try: 실행 중 발생할 수 있는 오류를 처리하기 위한 구문
            try:

                # split(): 공백을 기준으로 문자열 나누기
                # 예: "1 2 3" → ["1", "2", "3"]
                #
                # map(float, ...): 각 문자열을 실수로 변환
                # list(): 변환 결과를 리스트로 만들기
                # 결과: [1.0, 2.0, 3.0]
                row = list(map(float, text.split()))

                # 입력한 숫자가 정확히 3개인지 확인
                if len(row) != 3:
                    print("오류: 숫자를 정확히 3개 입력하세요.")

                    # continue: 현재 반복의 나머지를 건너뛰고
                    # while문 처음으로 돌아가 다시 입력받기
                    continue

                # 올바르게 입력된 행만 추가
                matrix.append(row)

                # break: while문 종료 후 다음 행으로 이동
                break

            # float()로 변환할 수 없는 문자가 들어오면 실행
            except ValueError:
                print("오류: 숫자만 입력하세요.")

    return matrix
