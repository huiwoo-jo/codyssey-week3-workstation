# modes/mode_pattern_generator.py

import time
from utils.utils import (
    display_matrix_terminal,
    normalize_label,
    validate_dimensions,
    generate_pattern
)

from utils.mac_ops import (
    compute_mac,
    compute_mac_1d,
    flatten_matrix,
    decide_winner,
    EPSILON
)

# ------------------------------------------
# [모드 3] N x N 패턴 자동 생성기 모드
# ------------------------------------------

def run_pattern_generator():
    print("\n#---------------------------------------")
    print("# [모드 3] N x N 패턴 자동 생성기")
    print("#---------------------------------------")

    # 1. 크기 입력
    try:
        N = int(input("생성할 필터 및 입력 크기 N 입력 (예: 5): ").strip())
        if N < 3:
            print("크기 N은 3 이상이어야 합니다.")
            return
    except ValueError:
        print("올바른 숫자를 입력하세요.")
        return

    # 2. N x N 크기의 기준 필터 2개(Cross, X) 자동 생성
    cross_filter = generate_pattern(N, "Cross")
    x_filter = generate_pattern(N, "X")

    print(f"\n✓ {N}x{N} 크기의 Cross 필터 및 X 필터가 자동으로 생성되었습니다.")
    display_matrix_terminal(cross_filter, name=f"생성된 {N}x{N} Cross 필터")
    display_matrix_terminal(x_filter, name=f"생성된 {N}x{N} X 필터")

    # 3. 재활용 모드 선택
    print("\n[재활용 모드 선택]")
    print(
        f"1. {N}x{N} 사용자 입력 데이터 받기 및 필터 비교 (모드 1 재활용)"
    )
    print(f"2. {N}x{N} 1D vs 2D 메모리 성능 분석 (성능 분석 재활용)")
    print("3. 메인 메뉴로 복귀")

    choice = input("선택: ").strip()

    if choice == "1":
        # 4. 사용자 입력에 맞춰 N x N 입력 데이터 생성/입력받기
        print(f"\n[4. {N}x{N} 사용자 입력 데이터 준비]")
        print("1) 테스트용 N x N Cross 입력 데이터 사용")
        print("2) 테스트용 N x N X 입력 데이터 사용")
        # N이 작을 경우 직접 타이핑 입력을 허용하도록 확장 가능
        input_type = input("입력 패턴 선택 (1 또는 2): ").strip()

        if input_type == "2":
            user_input_matrix = generate_pattern(N, "X")
            input_name = f"{N}x{N} X 입력 데이터"
        else:
            user_input_matrix = generate_pattern(N, "Cross")
            input_name = f"{N}x{N} Cross 입력 데이터"

        print(f"\n✓ 입력 데이터가 준비되었습니다.")
        display_matrix_terminal(user_input_matrix, name=input_name)

        # 5. 필터 비교 & 6. 결과 출력
        score_cross = compute_mac(user_input_matrix, cross_filter)
        score_x = compute_mac(user_input_matrix, x_filter)
        winner = decide_winner(score_cross, score_x)

        print("\n#=======================================")
        print(f"# [최종 결과] {N}x{N} 패턴 비교 결과")
        print("#=======================================")
        print(f"- Cross 필터 MAC 점수 : {score_cross}")
        print(f"- X 필터 MAC 점수     : {score_x}")
        print(f"- 최종 판정 결과      : {winner}")
        print("#=======================================\n")

    elif choice == "2":
        # 성능 분석 방식 재활용 (N x N 입력 데이터와 생성된 필터 활용)
        print(f"\n[4. {N}x{N} 성능 분석용 입력 데이터 자동 설정]")
        user_input_matrix = generate_pattern(N, "Cross")

        print(
            f"\n# [성능 분석 결과: {N}x{N} 크기 1D vs 2D MAC 연산 벤치마크 (100회)]"
        )

        f_1d = flatten_matrix(cross_filter)
        p_1d = flatten_matrix(user_input_matrix)

        iterations = 100

        # 2D 연산
        t0 = time.perf_counter()
        for _ in range(iterations):
            _ = compute_mac(user_input_matrix, cross_filter)
        t_2d_ms = ((time.perf_counter() - t0) / iterations) * 1000.0

        # 1D 연산
        t1 = time.perf_counter()
        for _ in range(iterations):
            _ = compute_mac_1d(p_1d, f_1d)
        t_1d_ms = ((time.perf_counter() - t1) / iterations) * 1000.0

        improvement = (
            ((t_2d_ms - t_1d_ms) / t_2d_ms) * 100.0 if t_2d_ms > 0 else 0.0
        )

        print(f"- 2차원 List 구조 연산 시간 : {t_2d_ms:.4f} ms")
        print(f"- 1차원 Flat Memory 연산 시간: {t_1d_ms:.4f} ms")
        print(f"- 메모리 연속성 최적화 개선율: {improvement:.1f}%")