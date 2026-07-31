# main.py

from modes import run_mode_1, run_mode_2, run_mode_pattern_generator

def main():
    # 모드 안내
    print("=== Mini NPU Simulator ===")
    print("\n[모드 선택]")
    print("1. 사용자 직접 입력 (3x3)")
    print("2. data.json 일괄 분석 및 성능 벤치마크")
    print("3. N x N 패턴 자동 생성기")
    
    # 모드 선택
    choice = input("선택: ").strip()
    if choice == '1':
        run_mode_1()
    elif choice == '2':
        run_mode_2()
    elif choice == '3':
        run_mode_pattern_generator()
    else:
        print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()