
# ============================================================
# 파일명: performance.py
# 설명: Mini NPU의 MAC 연산 성능을 측정하는 파일
#
# 주요 기능
# 1. MAC 연산을 최소 10회 반복 실행
# 2. 평균 실행 시간을 밀리초(ms) 단위로 계산
# 3. 배열 크기에 따른 MAC 누적 연산 횟수 계산
# 4. 성능 측정 결과를 화면에 출력
#
# 측정 대상: MAC 함수 실행 시간
# 입력이나 화면 출력 시간은 측정에서 제외
# ============================================================

# Python에서 시간을 측정할 때 사용하는 기본 모듈
import time

from mac import mac_score
from matrix import validate_matrix


# [함수] measure_performance(pattern, filter_matrix, runs)
# 기능: MAC 연산을 여러 번 실행하여 평균 시간을 측정한다.
#
# pattern: 입력 배열
# filter_matrix: 필터 배열
# runs: 반복 횟수 (기본값 10회)
#
# 반환값: 평균 실행 시간(ms), MAC 누적 연산 횟수
def measure_performance(pattern, filter_matrix, runs=10):

    # 패턴의 행 개수를 가져오기
    n = len(pattern) if isinstance(pattern, list) else 0

    # 올바른 정사각형 배열인지 확인
    if n == 0 or not validate_matrix(pattern, n):
        raise ValueError("패턴 배열 크기가 올바르지 않습니다.")

    if not validate_matrix(filter_matrix, n):
        raise ValueError("필터 배열 크기가 올바르지 않습니다.")

    # 최소 10회 이상 실행하도록 검사
    if type(runs) is not int or runs < 10:
        raise ValueError("성능 측정은 최소 10회 실행해야 합니다.")

    # perf_counter(): 경과 시간을 정밀하게 측정하는 함수
    # 시작 시간을 기록
    start = time.perf_counter()

    # MAC 연산을 runs 횟수만큼 반복
    for i in range(runs):
        mac_score(pattern, filter_matrix)

    # 종료 시간을 기록
    end = time.perf_counter()

    # end - start: 전체 실행 시간(초)
    # / runs: 1회 평균 실행 시간(초)
    # * 1000: 초를 밀리초(ms)로 변환
    average_ms = (end - start) / runs * 1000

    # n×n 배열의 MAC 누적 단계 수
    # 예: 5×5 = 25회
    operations = n * n

    return average_ms, operations


# [함수] print_performance(n, pattern, filter_matrix)
# 기능: MAC 성능을 측정하고 결과를 화면에 출력한다.
#
# n: 출력할 배열 크기
# pattern: 입력 배열
# filter_matrix: 필터 배열
def print_performance(n, pattern, filter_matrix):

    # 반환된 두 값을 각각의 변수에 저장
    average_ms, operations = measure_performance(
        pattern, filter_matrix, runs=10
    )

    # :.6f는 소수점 아래 여섯 자리까지 표시한다는 뜻
    print(
        f"{n}×{n} | "
        f"연산 횟수: {operations} | "
        f"평균 시간: {average_ms:.6f} ms"
    )
