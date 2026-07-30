def generate_pattern(N, pattern_type="Cross"):
    """
    [추가 과제 2] 크기 N에 대해 N x N 크기의 Cross(+) 또는 X 패턴 자동 생성
    """
    matrix = [[0.0] * N for _ in range(N)]

    if pattern_type.lower() in ["cross", "+"]:
        mid = N // 2
        for r in range(N):
            for c in range(N):
                if r == mid or c == mid:
                    matrix[r][c] = 1.0
                if N % 2 == 0:  # N이 짝수인 경우
                    if r == mid - 1 or c == mid - 1:
                        matrix[r][c] = 1.0

    elif pattern_type.lower() in ["x"]:
        for i in range(N):
            matrix[i][i] = 1.0
            matrix[i][N - 1 - i] = 1.0

    return matrix