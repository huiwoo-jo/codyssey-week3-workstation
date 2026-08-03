# codyssey-week3-workstation

## 1. 프로젝트 개요

- **코디세이 AI 입학 연수 2기 3주차**
- **Mission E01-3** AI가 계산하는 방식을 흉내 내는 작은 계산기 만들기

<br/>

## 2. 실행 환경 및 실행 방법

### 실행 환경
- **Language:** Python 3.14.6
- **Database/Dataset:** JSON (`data.json`)

### 실행 방법

프로젝트 루트 디렉토리에서 아래 명령어를 실행합니다.

```bash
python main.py
```

<br/>

## 3. 주요 기능

- **Pure Python MAC 연산 Engine:** 외부 라이브러리 없이 이중 반복문 기반 $2D$ 및 단일 반복문 기반 $1D$ MAC 연산 구현 ($O(N^2)$ 시간 복잡도)
- **메모리 접근 최적화 (1D Flat Matrix):** $2D$ 리스트를 $1D$ 연속 메모리 구조로 평탄화(Flatten)하여 연산 효율 개선 및 성능 비교 벤치마크 제공
- **$N \times N$ 패턴 자동 생성기:** 임의의 크기 $N$에 대해 규칙 기반 Cross(+) 및 X 패턴 행렬 자동 생성 logic
- **부동소수점 오차 보정 (Epsilon Handling):** 점수 차이가 $10^{-9}$ 미만인 미세한 차이는 동점(`UNDECIDED`)으로 안전 처리
- **유연한 라벨 정규화 (Label Normalization):** `+`, `cross`, `x` 등 다양한 입력 라벨을 표준 형식(`Cross`, `X`)으로 자동 변환
- **3가지 실행 모드 CLI 제공:**
  1. **사용자 직접 입력 모드 (3×3):** 콘솔에서 3×3 행렬을 직접 입력받아 MAC 연산 및 유사도 측정
  2. **일괄 분석 및 벤치마크 모드 (`data.json`):** JSON 데이터 일괄 판정, 1D/2D 연산 성능 벤치마크 리포트 출력
  3. **[추가 과제] 패턴 자동 생성기 모드:** 크기 $N$을 입력받아 패턴 생성 및 필터 상호작용 점수 시뮬레이션

<br/>

## 4. 수행 항목 체크리스트

### 기본 과제

* [x] 사용자 직접 입력 테스트 모드 (3×3)
* [x] `data.json` 기반 일괄 패턴 판정 및 검증 로직
* [x] Pure Python 기반 MAC 연산 기능
* [x] 부동소수점 오차 보정 (Epsilon $10^{-9}$ 적용)
* [x] 입력 라벨 정규화 (`+`, `cross` -> `Cross` / `x` -> `X`)
* [x] 행렬 차원 검증 및 예외 처리
* [x] 전체 테스트 수/통과 수/실패 수 및 실패 케이스 목록 요약
 
### 보너스 과제

* [x] **메모리 접근 최적화**: 2D 리스트의 1D 평탄화(Flatten) 및 1D MAC 연산 구현
* [x] **성능 벤치마크**: 크기별 2D vs 1D 연산 시간 비교 및 개선율 분석
* [x] **N×N 패턴 자동 생성기**: 임의의 $N \ge 3$ 크기에 대한 Cross/X 패턴 자동 생성 로직 구현
* [x] **코드 모듈화(Refactoring)**: 연산, 유틸리티, 모드 실행, 진입점 파일 분리


<br/>

## 5. 파일 및 디렉토리 구조

```text
CODYSSEY-WEEK3-WORKSTATION/
├── modes/                           # NPU 시뮬레이터 모드별 실행 로직 디렉토리
│   ├── mode_data_json.py            # [모드 2] data.json 기반 패턴 분석, 유효성 검증 & 1D/2D 성능 벤치마크
│   ├── mode_input_user.py           # [모드 1] 사용자 인터랙티브 직접 입력 기반 MAC 연산 및 패턴 분류
│   └── mode_pattern_generator.py    # [모드 3] N x N 크기별 동적 패턴 자동 생성 및 성능 실시간 분석
├── utils/                           # 공통 연산 엔진 및 헬퍼 모듈 디렉토리
│   ├── mac_ops.py                   # NPU 핵심 연산(2D/1D MAC, 승자 판정 decide_winner, 평탄화)
│   └── utils.py                     # 패턴 생성, 차원 검증 및 터미널 시각화 헬퍼
├── .gitattributes                   # Git 속성 관리 설정 파일
├── .gitignore                       # Git 추적 제외 파일 (__pycache__, 환경변수 등)
├── data.json                        # 크기별(3, 5, 13, 25) 필터 및 테스트 패턴 데이터셋
├── main.py                          # NPU 시뮬레이터 실행 Entry Point 및 메인 메뉴 루프
└── README.md                        # 프로젝트 설명 및 매뉴얼 문서
```

<br/>

## 6. 성능 측정 및 결과 분석

### 1. 메모리 접근 최적화 벤치마크 (2D vs 1D MAC 연산)

I/O 시간을 제외한 **순수 MAC 연산 시간**을 100회 반복 측정하여 평균 연산 시간 및 개선율을 산출한 결과입니다.

| **크기 ($N \times N$)** | **2차원 연산 (ms)** | **1차원 연산 (ms)** | **개선율 (%)** |
| --- | --- | --- | --- |
| **3 × 3** | 0.0010 ms | 0.0006 ms | **36.5%** |
| **5 × 5** | 0.0021 ms | 0.0015 ms | **27.6%** |
| **13 × 13** | 0.0117 ms | 0.0094 ms | **19.5%** |
| **25 × 25** | 0.0436 ms | 0.0404 ms | **7.3%%** |

> **성능 분석 결과**
> * $2D$ 리스트 접근(이중 인덱싱 `matrix[r][c]`) 대신 $1D$ 평탄화 리스트(단일 인덱싱 `flat[i]`)를 사용할 경우 오버헤드가 줄어들어 **약 20~35% 이상의 연산 속도 개선**을 보입니다.
> * 행렬의 크기가 커질수록 전체 연산 중 순수 arithmetic(곱셈·더하기) 연산 비중이 커지므로, 인덱싱 최적화에 따른 상대적 개선율(%)은 점차 감소하는 경향을 보입니다. 그러나 절대적인 시간 관점에서는 여전히 1D 접근 방식이 빠릅니다.
> 

---

### 2. `data.json` 일괄 테스트 결과 요약

* **전체 테스트 케이스:** 6개
* **통과 (PASS):** 3개 (`size_5_2`, `size_13_1`, `size_25_2`)
* **실패 (FAIL):** 3개 (`size_5_1`, `size_13_2`, `size_25_1`)


#### 🔍 `size_13_1` 실패 케이스 원인 분석
실패한 3개 케이스는 모두 Cross와 X 필터의 MAC 연산 결과 점수가 완전히 동일하게 나와 동점(`UNDECIDED`) 처리된 건입니다.
`size_5_1`: Cross(0.9) == X(0.9) → UNDECIDED (기대: X)
`size_13_2`: Cross(7.5) == X(7.5) → UNDECIDED (기대: Cross)
`size_25_1`: Cross(4.9) == X(4.9) → UNDECIDED (기대: X)

> **분석 결과**:  
> 모호하거나 대칭적인 입력 패턴에 대해 임의로 잘못된 예측을 내리지 않고, 부동소수점 임계값(`EPSILON`) 기준에 따라 안전하게 `UNDECIDED`로 예외 처리했음을 확인했습니다.

<br/>

## 7. 예외 처리 및 안정성 정책

1. **입력 형식 검증:** 콘솔 입력 시 숫자가 아니거나 3x3 규격에 맞지 않는 입력이 들어올 경우 오류 안내 문구를 출력하고 재입력을 유도합니다.
2. **행렬 차원 불일치 방지:** JSON 데이터 분석 시 정의된 크기 $N$과 실제 행렬의 행/열 길이가 일치하지 않으면 에러로 프로그램을 중단하지 않고 해당 케이스만 `FAIL` 처리 후 계속 진행합니다.
3. **부동소수점 비교 안전성:** 오차범위 `1e-9`를 적용하여 부동소수점 표현 한계로 인한 오판정을 방지합니다.
4. **라벨 데이터 정형화 (normalize_label):** JSON이나 사용자 입력 라벨의 대소문자 불일치(cross vs CROSS), 무작위 공백 포함 등의 예외를 표준화하여 라벨 단순 오기 입력으로 인한 판정 실패를 방지합니다.

<br/>

## 8. 실행 결과
### [MODE 1] 사용자 직접 입력 (3x3)
#### [A 필터]
<img width="1470" height="923" alt="image" src="https://github.com/user-attachments/assets/4274b879-172d-4e08-be4c-1cd6fc8435ff" />

#### [B 필터]
<img width="1470" height="923" alt="image" src="https://github.com/user-attachments/assets/c7e97f33-ed98-4625-a27f-eed77a2b789b" />


### [MODE2] data.json 일괄 분석 및 성능 벤치마크
<img width="1470" height="923" alt="image" src="https://github.com/user-attachments/assets/a59476c9-8a94-4330-a07f-b35d32f4438f" />


### [MDOE 3] N x N 패턴 자동 생성기
#### [필터 자동 생성]
<img width="1470" height="923" alt="image" src="https://github.com/user-attachments/assets/4851da26-a054-4ffb-bd92-f8ccb87b3357" />

#### 1. 5x5 사용자 입력 데이터 받기 및 필터 비교
#### 1-1. 테스트용 N x N Cross 입력 데이터 사용
<img width="1470" height="923" alt="image" src="https://github.com/user-attachments/assets/6d61f3c4-4cc8-483a-ae19-ad98aa8428bb" />

#### 1-2. 테스트용 N x N X 입력 데이터 사용
<img width="1470" height="923" alt="image" src="https://github.com/user-attachments/assets/ced738ad-e400-4a25-8e69-7d48bae3f556" />

### 2. 5x5 1D vs 2D 메모리 성능 분석
<img width="1470" height="923" alt="image" src="https://github.com/user-attachments/assets/11ce3dd4-2427-407c-934f-53afdfcdced9" />

