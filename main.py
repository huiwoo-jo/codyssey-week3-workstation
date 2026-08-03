# main.py

from modes.mode_data_json import run_data_json
from modes.mode_input_user import run_input_user
from modes.mode_pattern_generator import run_pattern_generator

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
        run_input_user()
    elif choice == '2':
        run_data_json()
    elif choice == '3':
        run_pattern_generator()
    else:
        print("잘못된 선택입니다.")
            
        
if __name__ == "__main__":
    main()