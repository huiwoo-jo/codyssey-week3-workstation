# utils/utils.py
# 원하는 크기 N×N을 지정하면 십자가(Cross)나 대각선(X) 형태의 행렬을 알아서 만들어주는 패턴 자동 생성 함수

# 입력 라벨 표준화
def normalize_label(label_str):
    """입력 라벨을 표준 라벨(Cross, X)로 정규화"""
    s = str(label_str).strip().lower()
    
    if s in ['+', 'cross']:
        return "Cross"
    elif s in ['x']:
        return "X"
    return label_str

# 행렬 크기 검증
def validate_dimensions(matrix, expected_size):
    """행렬 크기 검증"""
    if len(matrix) != expected_size:
        return False
    for row in matrix:
        if len(row) != expected_size:
            return False
    return True

# 입력받은 크기 N에 대해 N x N 크기의 Cross(+) 또는 X 패턴 자동 생성, 기본 값은 Cross(+)
# pattern 입력값: +, Cross, cross / x, X
def generate_pattern(N, pattern_type="Cross"):
    """
    [추가 과제 2] 크기 N에 대해 N x N 크기의 Cross(+) 또는 X 패턴 자동 생성
    """
    # 리스트 컴프리핸션을 사용해 모든 요소가 0.0으로 채워진 N×N 크기의 2차원 리스트 생성
    matrix = [[0.0] * N for _ in range(N)]

    # [+ 생성 로직] "cross", "Cross", "+"을 cross로 생성
    if normalize_label(pattern_type) is "Cross":
        # 가운데 값 판정
        mid = N // 2

        for r in range(N):
            for c in range(N):
                if r == mid or c == mid:
                    matrix[r][c] = 1.0
                if N % 2 == 0:  # N이 짝수인 경우 선 2줄
                    if r == mid - 1 or c == mid - 1:
                        matrix[r][c] = 1.0

    # [x 생성 로직]
    elif normalize_label(pattern_type) is "X":
        for r in range(N):
            for c in range(N):
                # X자 모양: 주대각선(r == c) 또는 반대각선(r + c == N - 1)
                if r == c or (r + c == N - 1):
                    matrix[r][c] = 1.0

    # 결과 반환
    return matrix


def display_matrix_terminal(matrix, name="Matrix", max_display_size=15):
    """N x N 행렬을 터미널에 텍스트 그래픽(■/□) 및 숫자 그리드로 시각화 출력하는 함수"""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    print(f"\n┌──────────────────────────────────────────────┐")
    print(f"│     {name} ({rows}x{cols})")
    print(f"└──────────────────────────────────────────────┘")

    # N이 너무 크면 화면이 깨지므로 텍스트 그래픽 및 핵심 영역만 출력
    if rows > max_display_size:
        print(
            f"※ 크기({rows}x{cols})가 커서 패턴 그래픽 요약본(상단 10x10)만 표시합니다.\n"
        )
        display_rows, display_cols = 10, 10
    else:
        display_rows, display_cols = rows, cols

    print("< 패턴 형상 Map (■: Activation / □: Zero) >")
    for r in range(display_rows):
        line = " ".join("■" if matrix[r][c] != 0 else "□" for c in range(display_cols))
        if cols > display_cols:
            line += " ..."
        print(f"  {line}")
    if rows > display_rows:
        print("  " + " : " * display_cols)