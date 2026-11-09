"""
냉장고 식재료 유통기한 관리 및 레시피 추천 프로그램
"""
from datetime import datetime

# 저장 구조
inventory = []

# 레시피 데이터베이스
recipes = {
    "계란볶음밥": ["계란", "밥", "대파"],
    "김치찌개": ["김치", "돼지고기", "두부"],
    "두부조림": ["두부", "대파", "간장"],
    "토마토 계란볶음": ["계란", "토마토", "대파"]
}

def register_ingredient():
    """식재료 등록 함수"""
    print("\n[ 📝 식재료 등록 ]")
    name = input("식재료 이름을 입력하세요: ").strip()
    if not name:
        print("❌ 식재료 이름은 비어있을 수 없습니다.")
        return
        
    expiry_str = input("유통기한을 입력하세요 (YYYY-MM-DD): ").strip()
    
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        inventory.append({"name": name, "expiry": expiry_date})
        print(f"✅ '{name}' (유통기한: {expiry_date}) 등록이 완료되었습니다.")
    except ValueError:
        print("❌ 날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.")

def check_expiration():
    """유통기한 현황 조회 함수"""
    if not inventory:
        print("\n⚠️ 현재 등록된 식재료가 없습니다.")
        return
        
    today = datetime.now().date()
    print("\n[ 🛒 식재료 유통기한 현황 ]")
    
    # 남은 D-Day 기준으로 오름차순 정렬
    sorted_inventory = sorted(inventory, key=lambda x: x["expiry"])
    
    for item in sorted_inventory:
        d_day = (item["expiry"] - today).days
        if d_day < 0:
            status = f"⚠️ 유통기한 경과 ({abs(d_day)}일 경과)"
        elif d_day <= 3:
            status = f"🚨 소비 임박 (D-{d_day})"
        else:
            status = f"✅ 여유 (D-{d_day})"
            
        print(f"- {item['name']}: {item['expiry']} [{status}]")

def recommend_recipes():
    """보유 식재료 기반 레시피 추천 함수"""
    if not inventory:
        print("\n⚠️ 등록된 식재료가 없습니다. 먼저 식재료를 등록해주세요.")
        return

    available_ingredients = set(item["name"] for item in inventory)
    print("\n[ 🍳 보유 재료 기반 추천 레시피 ]")
    
    matched = False
    for recipe_name, required in recipes.items():
        has_ingredients = set(required).intersection(available_ingredients)
        match_rate = len(has_ingredients) / len(required)
        
        # 보유 재료가 필요 재료의 50% 이상일 때 추천
        if match_rate >= 0.5:
            matched = True
            missing = set(required) - available_ingredients
            print(f"👉 {recipe_name} (보유 중: {list(has_ingredients)})")
            if missing:
                print(f"   └ 부족한 재료: {list(missing)}")
                
    if not matched:
        print("현재 보유한 재료로 조리 가능한 레시피가 없습니다.")

def main():
    """메인 실행 루프"""
    while True:
        print("\n" + "="*40)
        print(" 🧊 냉장고 식재료 관리 & 레시피 추천 시스템")
        print("="*40)
        print("1. 식재료 등록")
        print("2. 유통기한 현황 조회")
        print("3. 보유 재료 기반 레시피 추천")
        print("4. 종료")
        print("="*40)
        
        choice = input("선택할 메뉴 번호를 입력하세요: ").strip()
        
        if choice == "1":
            register_ingredient()
        elif choice == "2":
            check_expiration()
        elif choice == "3":
            recommend_recipes()
        elif choice == "4":
            print("\n프로그램을 종료합니다. 이용해주셔서 감사합니다!")
            break
        else:
            print("\n❌ 올바른 메뉴 번호를 선택해 주세요 (1~4).")

if __name__ == "__main__":
    main()
