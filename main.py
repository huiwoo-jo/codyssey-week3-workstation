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