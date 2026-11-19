
# ============================================================
# 파일명: main.py
# 설명: Mini NPU 시뮬레이터의 메인 실행 파일
#
# 주요 기능
# 1. 프로그램 메뉴 출력
# 2. 모드 1: 사용자가 직접 3×3 배열 입력
# 3. 모드 2: data.json 파일을 읽어 자동 분석
# 4. MAC 점수 및 최종 판정 출력
# 5. 성능 측정 및 PASS/FAIL 결과 출력
# 6. 프로그램 종료 처리
#
# 실행 방법: python3 main.py
# ============================================================

# JSON 파일을 읽기 위한 Python 기본 모듈
import json

# 다른 파일에 작성한 함수들을 가져오기
from matrix import create_matrix, input_matrix, validate_matrix
from mac import classify_pattern, normalize_label
from performance import print_performance


# [함수] load_data()
# 기능: data.json 파일을 읽어서 Python 데이터로 반환한다.
def load_data():

    # with: 파일 사용이 끝나면 자동으로 닫아 주는 구문
    # open(): 파일 열기
    # "r": 읽기 모드
    # encoding="utf-8": 문자 인코딩 지정
    # as file: 열린 파일을 file이라는 변수로 사용
    with open("data.json", "r", encoding="utf-8") as file:

        # json.load(): JSON 내용을 Python 자료형으로 변환
        data = json.load(file)

    return data


# [함수] show_menu()
# 기능: 사용자에게 프로그램의 메뉴를 보여준다.
def show_menu():
    print("\n===== Mini NPU Simulator =====")
    print("1. 직접 입력 모드")
    print("2. JSON 자동 분석 모드")
    print("0. 종료")


# [함수] run_mode1()
# 기능: 사용자가 필터 A, 필터 B, 입력 패턴을 직접 입력하고
#       MAC 점수를 계산하여 결과를 판정한다.
def run_mode1():
    print("\n[모드 1] 직접 입력")

    # input_matrix(): 3×3 배열을 사용자에게 입력받는 함수
    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")
    pattern = input_matrix("입력 패턴")

    # classify_pattern()은 점수 2개와 판정 결과를 반환
    # 각각 score_a, score_b, result에 저장
    score_a, score_b, result = classify_pattern(
        pattern, filter_a, filter_b
    )

    print("\n===== 분석 결과 =====")
    print(f"필터 A 점수: {score_a:.6f}")
    print(f"필터 B 점수: {score_b:.6f}")

    # 첫 번째 점수가 높으면 A
    # 두 번째 점수가 높으면 B
    # 점수가 거의 같으면 UNDECIDED
    if result == "Cross":
        print("최종 판정: A")

    elif result == "X":
        print("최종 판정: B")

    else:
        print("최종 판정: UNDECIDED")

    print("\n===== 성능 측정 =====")

    # 입력한 3×3 배열을 이용하여 성능 측정
    print_performance(3, pattern, filter_a)


# [함수] get_pattern_size(pattern_id)
# 기능: 패턴 ID에서 배열 크기를 추출한다.
#
# 예: "size_5_1" → 5
#     "size_13_2" → 13
def get_pattern_size(pattern_id):

    # ID가 문자열인지 확인
    if not isinstance(pattern_id, str):
        raise ValueError("패턴 ID가 문자열이 아닙니다.")

    # split("_"): 밑줄을 기준으로 문자열 나누기
    # "size_5_1" → ["size", "5", "1"]
    parts = pattern_id.split("_")

    # ID가 정해진 형식인지 검사
    if len(parts) != 3 or parts[0] != "size":
        raise ValueError("패턴 ID 형식 오류")

    # parts[1]은 "5" 같은 문자열
    # int()로 정수 5로 변환
    try:
        n = int(parts[1])
    except ValueError:
        raise ValueError("패턴 크기가 숫자가 아닙니다.")

    # 과제에서 지원하는 JSON 패턴 크기
    if n not in (5, 13, 25):
        raise ValueError("지원하지 않는 패턴 크기")

    return n


# [함수] run_mode2()
# 기능: JSON의 필터와 패턴을 읽어 자동 분석한다.
#
# 처리 순서
# 1. JSON 파일 읽기
# 2. 데이터 구조 확인
# 3. 패턴별 MAC 점수 계산
# 4. 예상 정답과 비교하여 PASS/FAIL 판정
# 5. 성능 측정
# 6. 전체 결과 요약
def run_mode2():
    print("\n[모드 2] JSON 자동 분석")

    # 파일이 없거나 JSON 문법이 잘못되었을 때 오류 처리
    try:
        data = load_data()

    # except: try 안에서 지정한 오류가 발생하면 실행
    # OSError: 파일 열기 등의 오류
    # JSONDecodeError: JSON 문법 오류
    except (OSError, json.JSONDecodeError) as error:
        print(f"JSON 파일 읽기 오류: {error}")
        return

    # JSON 최상위 데이터가 딕셔너리인지 검사
    if not isinstance(data, dict):
        print("JSON 데이터 구조 오류")
        return

    # get(): 딕셔너리에서 키에 해당하는 값 가져오기
    # 키가 없으면 기본적으로 None 반환
    filters = data.get("filters")
    patterns = data.get("patterns")

    if not isinstance(filters, dict):
        print("filters 데이터 구조 오류")
        return

    if not isinstance(patterns, dict):
        print("patterns 데이터 구조 오류")
        return

    # 결과를 누적할 변수
    total = 0
    passed = 0
    failed = 0

    # 실패 원인을 저장할 리스트
    failures = []

    print("\n===== 패턴 분석 결과 =====")

    # items(): 딕셔너리의 키와 값을 함께 가져옴
    #
    # 예:
    # pattern_id = "size_5_1"
    # pattern_info = {"input": [...], "expected": "x"}
    for pattern_id, pattern_info in patterns.items():

        # 검사한 패턴 개수 1 증가
        total += 1

        try:
            # 패턴 ID에서 배열 크기 추출
            n = get_pattern_size(pattern_id)

            # 각 패턴의 데이터 구조 검사
            if not isinstance(pattern_info, dict):
                raise ValueError("패턴 데이터 형식 오류")

            # 실제 입력 배열 가져오기
            pattern = pattern_info.get("input")

            # 예상 정답을 Cross 또는 X 형태로 통일
            expected = normalize_label(
                pattern_info.get("expected")
            )

            if expected is None:
                raise ValueError("정답 레이블 오류")

            # 패턴 배열의 행·열 크기와 숫자 검사
            if not validate_matrix(pattern, n):
                raise ValueError("패턴 배열 크기 또는 값 오류")

            # f문자열을 이용해 필터 키 생성
            # 예: n=5이면 "size_5"
            size_key = f"size_{n}"

            # 해당 크기의 필터 가져오기
            filter_group = filters.get(size_key)

            if not isinstance(filter_group, dict):
                raise ValueError("해당 크기의 필터가 없습니다")

            # Cross 필터와 X 필터 가져오기
            filter_cross = filter_group.get("cross")
            filter_x = filter_group.get("x")

            # 필터 크기와 값 검사
            if not validate_matrix(filter_cross, n):
                raise ValueError("Cross 필터 오류")

            if not validate_matrix(filter_x, n):
                raise ValueError("X 필터 오류")

            # MAC 점수 계산 및 최종 판정
            score_cross, score_x, result = classify_pattern(
                pattern, filter_cross, filter_x
            )

            # 계산 결과와 JSON의 예상 정답 비교
            if result == expected:
                status = "PASS"
                passed += 1

            else:
                status = "FAIL"
                failed += 1

                # append(): 실패 내용을 리스트에 추가
                failures.append(
                    f"{pattern_id}: 예상 {expected}, 실제 {result}"
                )

            # 개별 패턴 결과 출력
            print(f"\n패턴 ID: {pattern_id}")
            print(f"Cross 점수: {score_cross:.6f}")
            print(f"X 점수: {score_x:.6f}")
            print(f"예상 정답: {expected}")
            print(f"판정 결과: {result}")
            print(f"검사 결과: {status}")

        # 특정 패턴에서 오류가 나더라도
        # 프로그램을 종료하지 않고 다음 패턴을 검사
        except (ValueError, TypeError, KeyError) as error:
            failed += 1
            failures.append(f"{pattern_id}: {error}")

            print(f"\n패턴 ID: {pattern_id}")
            print("검사 결과: FAIL")
            print(f"오류 원인: {error}")

    print("\n===== 성능 측정 =====")

    # JSON에는 3×3 필터가 없으므로 테스트 배열 생성
    test_matrix = create_matrix(3)

    # 3×3 성능 측정
    print_performance(3, test_matrix, test_matrix)

    # 5×5, 13×13, 25×25 성능 측정
    for n in [5, 13, 25]:

        try:
            # 해당 크기의 필터 그룹 가져오기
            filter_group = filters.get(f"size_{n}")

            if not isinstance(filter_group, dict):
                raise ValueError("필터 데이터 없음")

            # Cross 필터를 성능 측정용으로 사용
            filter_cross = filter_group.get("cross")

            if not validate_matrix(filter_cross, n):
                raise ValueError("필터 배열 오류")

            # MAC 연산 10회 실행 후 평균 시간 출력
            print_performance(n, filter_cross, filter_cross)

        except (ValueError, TypeError) as error:
            print(f"{n}×{n} 성능 측정 실패: {error}")

    print("\n===== 최종 결과 요약 =====")
    print(f"전체 패턴: {total}")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")

    # 실패 목록에 데이터가 있으면 출력
    if failures:
        print("\n실패 목록:")

        for failure in failures:
            print(f"- {failure}")

    else:
        print("실패한 패턴이 없습니다.")


# [함수] main()
# 기능: 프로그램의 메뉴를 반복 출력하고
#       사용자가 선택한 기능을 실행한다.
def main():

    # 종료 메뉴를 선택하기 전까지 반복
    while True:
        show_menu()

        # strip(): 입력값 앞뒤의 공백 제거
        choice = input("\n메뉴 선택: ").strip()

        if choice == "1":
            run_mode1()

        elif choice == "2":
            run_mode2()

        elif choice == "0":
            print("프로그램을 종료합니다.")

            # break: while문 종료
            break

        else:
            print("올바른 메뉴 번호를 입력하세요.")


# 이 파일을 직접 실행했을 때만 main() 호출
# 다른 파일에서 import할 때는 자동 실행되지 않음
if __name__ == "__main__":

    try:
        main()

    # Ctrl+C 또는 입력 종료 신호를 처리
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
