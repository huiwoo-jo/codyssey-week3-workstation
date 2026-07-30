import time
import json
import sys

EPSILON = 1e-9

def compute_mac(pattern, filter_matrix):
    """
    외부 라이브러리(NumPy 등) 없이 2차원 배열의 MAC 연산을 수행합니다.
    """
    score = 0.0
    rows = len(pattern)
    cols = len(pattern[0])
    for r in range(rows):
        for c in range(cols):
            score += float(pattern[r][c]) * float(filter_matrix[r][c])
    return score

def decide_winner(score_cross, score_x):
    """
    abs(score_cross - score_x) < 1e-9 이면 UNDECIDED,
    그 외 점수가 높은 라벨(Cross 또는 X)을 반환합니다.
    """
    diff = abs(score_cross - score_x)
    if diff < EPSILON:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"
    
def normalize_label(label_str):
    """
    입력된 라벨을 표준 라벨(Cross, X)로 정규화합니다.
    """
    s = str(label_str).strip().lower()
    if s in ['+', 'cross']:
        return "Cross"
    elif s in ['x']:
        return "X"
    return label_str  # 매칭되지 않으면 원본 반환

def validate_dimensions(matrix, expected_size):
    """
    행렬의 행/열 크기가 expected_size x expected_size와 일치하는지 검증합니다.
    """
    if len(matrix) != expected_size:
        return False
    for row in matrix:
        if len(row) != expected_size:
            return False
    return True

def input_matrix_3x3(prompt_name):
    """
    3x3 행렬을 사용자 콘솔에서 한 줄씩 입력받고 유효성을 검증합니다.
    """
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
    print("# [1] 필터 입력")
    print("#----------------------------------------")
    filter_a = input_matrix_3x3("필터 A")
    filter_b = input_matrix_3x3("필터 B")

    print("\n#----------------------------------------")
    print("# [2] 패턴 입력")
    print("#----------------------------------------")
    pattern = input_matrix_3x3("패턴")

    print("\n#----------------------------------------")
    print("# [3] MAC 결과")
    print("#----------------------------------------")
    
    # 10회 반복 측정하여 I/O 제외 연산 평균 시간 측정
    iterations = 10
    start_t = time.perf_counter()
    for _ in range(iterations):
        score_a = compute_mac(pattern, filter_a)
        score_b = compute_mac(pattern, filter_b)
    end_t = time.perf_counter()
    
    avg_time_ms = ((end_t - start_t) / iterations) * 1000.0
    
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time_ms:.3f} ms")
    
    diff = abs(score_a - score_b)
    if diff < EPSILON:
        print(f"판정: 판정 불가 (|A-B| < 1e-9)")
    elif score_a > score_b:
        print("판정: A")
    else:
        print("판정: B")

def load_json_data(filepath="data.json"):
    """
    json 파일을 로드하고 스키마 기본 구조를 반환합니다.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"파일 로드 실패: {e}")
        return None