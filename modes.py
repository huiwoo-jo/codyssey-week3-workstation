# modes.py

import time
import json
from utils import (
    normalize_label,
    validate_dimensions,
    generate_pattern
)

from mac_ops import (
    compute_mac,
    compute_mac_1d,
    flatten_matrix,
    decide_winner,
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

def run_mode_1():
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


# ------------------------------------------
# [모드 2] data.json 일괄 분석 & 벤치마크
# ------------------------------------------

def load_json_data(filepath="data.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"파일 로드 실패: {e}")
        return None

def process_data_json_cases(data):
    filters_dict = data.get("filters", {})
    patterns_dict = data.get("patterns", {})

    print("\n#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    for size_key in filters_dict:
        print(f"✓ {size_key:<7} 필터 로드 완료 (Cross, X)")

    print("\n#---------------------------------------")
    print("# [2] 패턴 분석")
    print("#---------------------------------------")

    results = []
    for case_id, pattern_info in patterns_dict.items():
        try:
            N = int(case_id.split("_")[1])
        except Exception:
            results.append({"id": case_id, "status": "FAIL", "reason": "키 크기 파싱 실패"})
            continue

        filter_group_key = f"size_{N}"
        if filter_group_key not in filters_dict:
            results.append({"id": case_id, "status": "FAIL", "reason": f"크기 {N} 필터 없음"})
            continue

        cross_filter = filters_dict[filter_group_key].get("cross")
        x_filter = filters_dict[filter_group_key].get("x")
        pattern_input = pattern_info.get("input")
        expected = normalize_label(pattern_info.get("expected"))

        if not (validate_dimensions(pattern_input, N) and 
                validate_dimensions(cross_filter, N) and 
                validate_dimensions(x_filter, N)):
            print(f"- -- {case_id} --- FAIL (크기 불일치)")
            results.append({"id": case_id, "status": "FAIL", "reason": f"크기 불일치 ({N}x{N})"})
            continue

        score_cross = compute_mac(pattern_input, cross_filter)
        score_x = compute_mac(pattern_input, x_filter)
        predicted = decide_winner(score_cross, score_x)

        status = "PASS" if predicted == expected else "FAIL"
        reason = "" if status == "PASS" else (
            "동점(UNDECIDED) 처리" if predicted == "UNDECIDED" else f"예측({predicted}) != 기대({expected})"
        )

        print(f"- -- {case_id} ---")
        print(f"Cross 점수: {score_cross:.6f} | X 점수: {score_x:.6f}")
        print(f"판정: {predicted} | expected: {expected} | [{status}]")

        results.append({"id": case_id, "status": status, "predicted": predicted, "expected": expected, "reason": reason})

    return results, filters_dict

def run_performance_benchmark(filters_dict):
    """기본 크기별 성능 분석 및 메모리 접근 최적화(1D vs 2D) 성능 비교"""
    print("\n#---------------------------------------")
    print("# [3] 성능 분석 & 메모리 접근 최적화 비교 (100회 평균)")
    print("#---------------------------------------")
    print(f"{'크기':<8} {'2차원 연산(ms)':<15} {'1차원 연산(ms)':<15} {'개선율':<10}")
    print("-" * 52)

    test_sizes = [3, 5, 13, 25]
    iterations = 100

    for N in test_sizes:
        filter_key = f"size_{N}"
        if filter_key in filters_dict:
            f_2d = filters_dict[filter_key]["cross"]
        else:
            f_2d = [[1.0] * N for _ in range(N)]
        p_2d = f_2d

        f_1d = flatten_matrix(f_2d)
        p_1d = flatten_matrix(p_2d)

        # 2차원 측정
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = compute_mac(p_2d, f_2d)
        t_2d_ms = ((time.perf_counter() - t0) / iterations) * 1000.0

        # 1차원 측정
        t1 = time.perf_counter()
        for _ in range(iterations):
            _ = compute_mac_1d(p_1d, f_1d)
        t_1d_ms = ((time.perf_counter() - t1) / iterations) * 1000.0

        improvement = ((t_2d_ms - t_1d_ms) / t_2d_ms) * 100.0 if t_2d_ms > 0 else 0.0
        print(f"{f'{N}x{N}':<8} {t_2d_ms:<15.4f} {t_1d_ms:<15.4f} {improvement:>6.1f}%")

def print_summary_report(results):
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed

    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total}개 | 통과: {passed}개 | 실패: {failed}개")
    if failed > 0:
        print("\n실패 상세:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"- {r['id']}: {r['reason']}")

def run_mode_2():
    data = load_json_data("data.json")
    if not data:
        return
    results, filters_dict = process_data_json_cases(data)
    run_performance_benchmark(filters_dict)
    print_summary_report(results)


# ------------------------------------------
# [추가 과제] N x N 패턴 자동 생성기 모드
# ------------------------------------------

def run_mode_pattern_generator():
    print("\n#---------------------------------------")
    print("# [추가 과제] N x N 패턴 자동 생성기 & 재활용")
    print("#---------------------------------------")
    try:
        N = int(input("생성할 패턴 크기 N 입력 (예: 10): ").strip())
        if N < 3:
            print("크기 N은 3 이상이어야 합니다.")
            return
    except ValueError:
        print("올바른 숫자를 입력하세요.")
        return

    # 1. 패턴 및 기본 필터 동적 생성
    generated_pattern = generate_pattern(N, "Cross")
    cross_filter = generate_pattern(N, "Cross")
    x_filter = generate_pattern(N, "X")

    print(f"\n✓ {N}x{N} 크기의 패턴 및 필터가 성공적으로 생성되었습니다.")

    # 2. 재활용 메뉴 선택
    print("\n[생성된 패턴 재활용 옵션]")
    print("1. 생성된 패턴으로 MAC 연산 및 유사도 판정 (모드 1 재활용)")
    print("2. 생성된 패턴으로 1D vs 2D 메모리 성능 벤치마크 (성능 분석 재활용)")
    print("3. 메인 메뉴로 복귀")
    
    sub_choice = input("선택: ").strip()

    if sub_choice == '1':
        # --- 모드 1 로직 재활용 ---
        score_cross = compute_mac(generated_pattern, cross_filter)
        score_x = compute_mac(generated_pattern, x_filter)
        winner = decide_winner(score_cross, score_x)
        
        print("\n# [재활용 결과: MAC 연산 & 판정]")
        print(f"- Cross 필터 점수: {score_cross}")
        print(f"- X 필터 점수    : {score_x}")
        print(f"- 최종 판정 결과 : {winner}")

    elif sub_choice == '2':
        # --- 성능 분석 로직 재활용 ---
        print(f"\n# [재활용 결과: {N}x{N} 크기 1D vs 2D 성능 벤치마크 (100회 평균)]")
        
        f_1d = flatten_matrix(cross_filter)
        p_1d = flatten_matrix(generated_pattern)

        iterations = 100
        # 2D 측정
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = compute_mac(generated_pattern, cross_filter)
        t_2d_ms = ((time.perf_counter() - t0) / iterations) * 1000.0

        # 1D 측정
        t1 = time.perf_counter()
        for _ in range(iterations):
            _ = compute_mac_1d(p_1d, f_1d)
        t_1d_ms = ((time.perf_counter() - t1) / iterations) * 1000.0

        improvement = ((t_2d_ms - t_1d_ms) / t_2d_ms) * 100.0 if t_2d_ms > 0 else 0.0
        
        print(f"2차원 연산 시간: {t_2d_ms:.4f} ms")
        print(f"1차원 연산 시간: {t_1d_ms:.4f} ms")
        print(f"메모리 최적화 개선율: {improvement:.1f}%")