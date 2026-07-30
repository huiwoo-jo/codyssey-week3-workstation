import time

EPSILON = 1e-9

def compute_mac(pattern, filter_matrix):
    """2차원 배열 기반 MAC 연산"""
    score = 0.0
    rows = len(pattern)
    cols = len(pattern[0])
    for r in range(rows):
        for c in range(cols):
            score += float(pattern[r][c]) * float(filter_matrix[r][c])
    return score

def flatten_matrix(matrix_2d):
    """[추가 과제 1] 2차원 리스트를 1차원 리스트로 평탄화"""
    flat = []
    for row in matrix_2d:
        flat.extend(row)
    return flat

def compute_mac_1d(pattern_1d, filter_1d):
    """[추가 과제 1] 1차원 리스트 기반 MAC 연산"""
    score = 0.0
    for i in range(len(pattern_1d)):
        score += float(pattern_1d[i]) * float(filter_1d[i])
    return score

def decide_winner(score_cross, score_x):
    """Epsilon 오차 범위를 고려한 승자 판정"""
    diff = abs(score_cross - score_x)
    if diff < EPSILON:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"

def normalize_label(label_str):
    """입력 라벨을 표준 라벨(Cross, X)로 정규화"""
    s = str(label_str).strip().lower()
    if s in ['+', 'cross']:
        return "Cross"
    elif s in ['x']:
        return "X"
    return label_str

def validate_dimensions(matrix, expected_size):
    """행렬 크기 검증"""
    if len(matrix) != expected_size:
        return False
    for row in matrix:
        if len(row) != expected_size:
            return False
    return True