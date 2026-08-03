# modes/mode_input_user.py

import time
from utils.mac_ops import (
    compute_mac,
    EPSILON
)

# ------------------------------------------
# [모드 1] 사용자 직접 입력 테스트 (3x3)
# ------------------------------------------

def input_matrix_3x3(prompt_name):
    print(f"\n{prompt_name} (3줄 입력, 공백 구분)")
    while True:
        matrix = []
        valid = True
        for i in range(3):
            line = input().strip()
            parts = line.split()
            if len(parts) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                valid = False
                break
            try:
                row = [float(x) for x in parts]
                matrix.append(row)
            except ValueError:
                print("입력 형식 오류: 숫자가 아닌 값이 포함되어 있습니다.")
                valid = False
                break
        if valid and len(matrix) == 3:
            return matrix

def run_input_user():
    print("\n#----------------------------------------")
    print("# [모드 1] 사용자 입력 테스트 (3x3)")
    print("#----------------------------------------")
    filter_a = input_matrix_3x3("필터 A (예: Cross 필터)")
    filter_b = input_matrix_3x3("필터 B (예: X 필터)")
    pattern = input_matrix_3x3("테스트 패턴")

    iterations = 10
    start_t = time.perf_counter()
    for _ in range(iterations):
        score_a = compute_mac(pattern, filter_a)
        score_b = compute_mac(pattern, filter_b)
    end_t = time.perf_counter()
    
    avg_time_ms = ((end_t - start_t) / iterations) * 1000.0
    
    print("\n#----------------------------------------")
    print("# 결과")
    print("#----------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time_ms:.3f} ms")
    
    diff = abs(score_a - score_b)
    if diff < EPSILON:
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    elif score_a > score_b:
        print("판정: A 필터 유사")
    else:
        print("판정: B 필터 유사")