# utils.py
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
    if normalize_label(pattern_type):
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
    elif normalize_label(pattern_type):
        for i in range(N):
            matrix[i][i] = 1.0 #좌측 상단
            matrix[i][N - 1 - i] = 1.0 # 우측 상단

    # 결과 반환
    return matrix