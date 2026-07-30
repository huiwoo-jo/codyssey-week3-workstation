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