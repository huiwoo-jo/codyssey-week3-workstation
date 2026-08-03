# modes/mode_data_json.py

import time
import json
from utils.mac_ops import (
    EPSILON,
    compute_mac,
    compute_mac_1d,
    decide_winner,
    flatten_matrix,
)
from utils.utils import normalize_label, validate_dimensions

# ------------------------------------------
# [모드 2] data.json 일괄 분석 & 벤치마크
# ------------------------------------------

def load_json_data(filepath="data.json"):
    """JSON 데이터 파일을 안전하게 로드합니다."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"파일 로드 실패 ({filepath}): {e}")
        return None


def process_data_json_cases(data):
    """JSON 데이터를 순회하며 필터와 패턴의 유사도를 분석하고 결과를 판정합니다."""
    filters_dict = data.get("filters", {})
    patterns_dict = data.get("patterns", {})

    print("\n#---------------------------------------")
    print("# [1] 필터 로드 및 검증")
    print("#---------------------------------------")
    for size_key, f_data in filters_dict.items():
        # 키 이름에서 크기(N) 추출 (예: 'size_5' -> 5)
        try:
            N = int(size_key.split("_")[1])
        except (IndexError, ValueError):
            print(f"✗ {size_key:<7} 필터 오류 (키 포맷 불일치)")
            continue

        cross_f = f_data.get("cross")
        x_f = f_data.get("x")

        # 실제 필터 데이터의 유효성 검증
        is_cross_valid = validate_dimensions(cross_f, N)
        is_x_valid = validate_dimensions(x_f, N)

        if is_cross_valid and is_x_valid:
            print(f"✓ {size_key:<7} 필터 로드 완료 (Cross, X)")
        else:
            invalid_targets = []
            if not is_cross_valid: invalid_targets.append("Cross")
            if not is_x_valid: invalid_targets.append("X")
            print(f"✗ {size_key:<7} 필터 손상됨 ({', '.join(invalid_targets)} 데이터 오류)")
    

    print("\n#---------------------------------------")
    print("# [2] 패턴 분석")
    print("#---------------------------------------")

    results = []
    for case_id, pattern_info in patterns_dict.items():
        if not isinstance(pattern_info, dict):
            results.append(
                {"id": case_id, "status": "FAIL", "reason": "패턴 구조 손상"}
            )
            print(f"- -- {case_id} --- FAIL (패턴 구조 손상)")
            continue

        # case_id 파싱 (예: 'pattern_5' -> 5)
        try:
            parts = case_id.split("_")
            N = int(parts[1]) if len(parts) > 1 else int(parts[0])
        except (ValueError, IndexError):
            results.append(
                {"id": case_id, "status": "FAIL", "reason": "키 크기 파싱 실패"}
            )
            print(f"- -- {case_id} --- FAIL (키 크기 파싱 실패)")
            continue

        filter_group_key = f"size_{N}"
        if filter_group_key not in filters_dict:
            results.append(
                {
                    "id": case_id,
                    "status": "FAIL",
                    "reason": f"크기 {N} 필터 없음",
                }
            )
            print(f"- -- {case_id} --- FAIL (크기 {N} 필터 없음)")
            continue

        group_filters = filters_dict[filter_group_key]
        cross_filter = group_filters.get("cross")
        x_filter = group_filters.get("x")
        pattern_input = pattern_info.get("input")
        expected = normalize_label(pattern_info.get("expected"))

        # 입력 데이터 및 필터 유효성 검증
        if (
            not cross_filter
            or not x_filter
            or not validate_dimensions(pattern_input, N)
            or not validate_dimensions(cross_filter, N)
            or not validate_dimensions(x_filter, N)
        ):
            print(f"- -- {case_id} --- FAIL (크기/구조 불일치)")
            results.append(
                {
                    "id": case_id,
                    "status": "FAIL",
                    "reason": f"크기 불일치 ({N}x{N})",
                }
            )
            continue

        # MAC 연산 및 승자 판정
        score_cross = compute_mac(pattern_input, cross_filter)
        score_x = compute_mac(pattern_input, x_filter)
        predicted = decide_winner(score_cross, score_x)

        status = "PASS" if predicted == expected else "FAIL"
        
        reason = (
            ""
            if status == "PASS"
            else (
                "동점(UNDECIDED) 처리"
                if predicted == "UNDECIDED"
                else f"예측({predicted}) != 기대({expected})"
            )
        )

        print(f"- -- {case_id} ---")
        print(f"Cross 점수: {score_cross:.6f} | X 점수: {score_x:.6f}")
        print(f"판정: {predicted} | expected: {expected} | [{status}]")

        results.append(
            {
                "id": case_id,
                "status": status,
                "predicted": predicted,
                "expected": expected,
                "reason": reason,
            }
        )

    return results, filters_dict

def run_performance_benchmark(filters_dict):
    """크기별 2차원 vs 1차원 연산 속도 및 메모리 접근 최적화 성능 비교"""
    print("\n#---------------------------------------")
    print("# [3] 성능 분석 & 메모리 접근 최적화 비교 (100회 평균)")
    print("#---------------------------------------")
    print(
        f"{'크기':<8} {'2차원 연산(ms)':<15} {'1차원 연산(ms)':<15} {'개선율':<10}"
    )
    print("-" * 52)

    test_sizes = [3, 5, 13, 25]
    iterations = 100

    for N in test_sizes:
        filter_key = f"size_{N}"
        f_2d = None

        # 1. 필터 존재 여부 및 유효성(크기/손상 여부) 엄격 검증
        if filter_key in filters_dict:
            candidate_f = filters_dict[filter_key].get("cross")
            if validate_dimensions(candidate_f, N):
                f_2d = candidate_f

        # 2. 필터가 없거나 손상된 경우 벤치마크용 기본 필터(1.0 채움) 생성
        if f_2d is None:
            f_2d = [[1.0] * N for _ in range(N)]

        p_2d = f_2d  # 테스트 패턴도 동일 필터 크기 기반으로 설정

        # 1D 평탄화
        f_1d = flatten_matrix(f_2d)
        p_1d = flatten_matrix(p_2d)

        # 2차원 연산 측정
        # 1. 측정 시작 시점의 타임스탬프 기록 (초 단위, float)
        t0 = time.perf_counter()

        # 2. MAC 연산을 K회 반복 (L1/L2 캐시 워밍업 효과 및 측정 안정화)
        for _ in range(iterations):
            _ = compute_mac(p_2d, f_2d)

        # 3. 측정 종료 시점의 타임스탬프 기록
        t_2d_ms = ((time.perf_counter() - t0) / iterations) * 1000.0

        # 1차원 연산 측정
        t1 = time.perf_counter()
        for _ in range(iterations):
            _ = compute_mac_1d(p_1d, f_1d)
        t_1d_ms = ((time.perf_counter() - t1) / iterations) * 1000.0

        improvement = (
            ((t_2d_ms - t_1d_ms) / t_2d_ms) * 100.0 if t_2d_ms > 0 else 0.0
        )
        print(
            f"{f'{N}x{N}':<8} {t_2d_ms:<15.4f} {t_1d_ms:<15.4f} {improvement:>6.1f}%"
        )

def print_summary_report(results):
    """분석 결과 요약을 출력합니다."""
    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = total - passed

    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total}개 | 통과: {passed}개 | 실패: {failed}개")

    if failed > 0:
        print("\n실패 상세:")
        for r in results:
            if r.get("status") == "FAIL":
                print(f"- {r['id']}: {r.get('reason', '알 수 없는 원인')}")


def run_data_json():
    """모드 2 전체 실행 진입점"""
    data = load_json_data("data.json")
    if not data:
        return
    results, filters_dict = process_data_json_cases(data)
    run_performance_benchmark(filters_dict)
    print_summary_report(results)