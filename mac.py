
# ============================================================
# 파일명: mac.py
# 설명: Mini NPU의 MAC 연산과 패턴 판정을 담당하는 파일
#
# 주요 기능
# 1. 입력 패턴과 필터의 MAC 점수 계산
# 2. 정답 레이블을 Cross / X 형태로 통일
# 3. 두 점수를 비교하여 최종 모양 판정
# 4. 점수 계산과 판정을 한 번에 수행
#
# MAC = Multiply-Accumulate
#     = 같은 위치의 값을 곱하고 결과를 계속 더하는 연산
# ============================================================

# 다른 파일(matrix.py)에 작성한 함수를 가져오기
from matrix import validate_matrix


# EPSILON: 실수 점수를 비교할 때 사용하는 허용 오차
# 1e-9는 0.000000001을 의미
EPSILON = 1e-9


# [함수] mac_score(pattern, filter_matrix)
# 기능: 입력 패턴과 필터의 같은 위치에 있는 숫자를
#       각각 곱한 후 모두 더해서 MAC 점수를 계산한다.
#
# pattern: 판별할 입력 배열
# filter_matrix: 비교 기준이 되는 필터 배열
# 반환값: 계산된 MAC 점수
def mac_score(pattern, filter_matrix):

    # len(): 리스트에 들어 있는 요소 개수 반환
    # 2차원 리스트에서는 바깥 리스트의 길이 = 행 개수
    n = len(pattern) if isinstance(pattern, list) else 0

    # 배열의 크기와 숫자 자료형이 올바른지 검사
    if n == 0 or not validate_matrix(pattern, n):
        # raise: 오류를 직접 발생시키는 명령어
        raise ValueError("패턴 배열이 올바르지 않습니다.")

    if not validate_matrix(filter_matrix, n):
        raise ValueError("필터 배열 크기가 올바르지 않습니다.")

    # MAC 결과를 누적할 변수
    score = 0.0

    # 바깥 for문: 행을 하나씩 이동
    for i in range(n):

        # 안쪽 for문: 현재 행의 열을 하나씩 이동
        for j in range(n):

            # 같은 위치의 패턴 값과 필터 값을 곱한 후 더하기
            # += 는 score = score + 계산값과 같은 의미
            score += pattern[i][j] * filter_matrix[i][j]

    return score


# [함수] normalize_label(label)
# 기능: JSON에 저장된 정답 표현을 하나의 형태로 통일한다.
#
# 예:
# "+"     → "Cross"
# "cross" → "Cross"
# "x"     → "X"
#
# 반환값: Cross / X / UNDECIDED 또는 None
def normalize_label(label):

    # 문자열이 아닌 데이터가 들어오면 처리하지 않음
    if not isinstance(label, str):
        return None

    # strip(): 문자열 앞뒤 공백 제거
    # lower(): 영문 대문자를 소문자로 변경
    label = label.strip().lower()

    # in: 여러 값 중 하나와 일치하는지 검사
    if label in ("+", "cross"):
        return "Cross"

    if label == "x":
        return "X"

    if label == "undecided":
        return "UNDECIDED"

    # None: 유효한 정답 표현이 없다는 의미
    return None


# [함수] decide(score_cross, score_x)
# 기능: 두 MAC 점수를 비교해서 최종 결과를 판정한다.
#
# 첫 번째 점수가 크면 Cross
# 두 번째 점수가 크면 X
# 두 점수의 차이가 EPSILON보다 작으면 UNDECIDED
def decide(score_cross, score_x):

    # abs(): 숫자의 절댓값을 구하는 함수
    # 점수 차이가 아주 작으면 동점으로 처리
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"

    if score_cross > score_x:
        return "Cross"

    return "X"


# [함수] classify_pattern(pattern, filter_cross, filter_x)
# 기능: 두 필터의 MAC 점수를 계산하고 최종 판정을 수행한다.
#
# 반환값: (첫 번째 필터 점수, 두 번째 필터 점수, 판정 결과)
#
# 모드 1에서는 첫 번째 필터=A, 두 번째 필터=B로 사용
# 모드 2에서는 첫 번째 필터=Cross, 두 번째 필터=X로 사용
def classify_pattern(pattern, filter_cross, filter_x):

    # 첫 번째 필터의 점수 계산
    score_cross = mac_score(pattern, filter_cross)

    # 두 번째 필터의 점수 계산
    score_x = mac_score(pattern, filter_x)

    # 두 점수를 비교해서 최종 판정
    result = decide(score_cross, score_x)

    # return에서 쉼표로 구분하면 여러 값을 함께 반환할 수 있음
    return score_cross, score_x, result
