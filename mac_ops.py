# mac_ops.py

# 부동 소수점 오차 기준 보정
EPSILON = 1e-9

def compute_mac(pattern, filter_matrix):
    """2차원 배열 기반 MAC 연산"""
    score = 0.0
    rows = len(pattern)
    cols = len(pattern[0])
    
    # 2중 반복문을 사용한 모든 행과 열 순회
    for r in range(rows):
        for c in range(cols):
            # 가중치 계산
            score += float(pattern[r][c]) * float(filter_matrix[r][c])
    return score

def flatten_matrix(matrix_2d):
    """[추가 과제 1] 2차원 리스트를 1차원 리스트로 평탄화"""
    flat = []
    for row in matrix_2d:
        flat.extend(row) # extend를 사용한 리스트 평탄화
    return flat

def compute_mac_1d(pattern_1d, filter_1d):
    """[추가 과제 1] 1차원 리스트 기반 MAC 연산"""
    score = 0.0

    # 단일 반복문을 사용한 순회
    for i in range(len(pattern_1d)):
        score += float(pattern_1d[i]) * float(filter_1d[i])
    return score

def decide_winner(score_cross, score_x):
    """Epsilon 오차 범위를 고려한 승자 판정"""
    diff = abs(score_cross - score_x)

    if diff < EPSILON:
        return "UNDECIDED" # 미세 소수점 차이로 인한 아주 작은 오차로 동일 판정
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"
