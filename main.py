import streamlit as st
from datetime import datetime

st.set_page_config(page_title="냉장고 식재료 관리", page_icon="🧊")

if "inventory" not in st.session_state:
    st.session_state.inventory = []

recipes = {
    "계란볶음밥": ["계란", "밥", "대파"],
    "김치찌개": ["김치", "돼지고기", "두부"],
    "두부조림": ["두부", "대파", "간장"],
    "토마토 계란볶음": ["계란", "토마토", "대파"]
}

st.title("🧊 냉장고 식재료 관리 & 레시피 추천")

# 1. 식재료 등록
st.header("1. 식재료 등록")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("식재료 이름")
with col2:
    expiry_date = st.date_input("유통기한 선택")

if st.button("식재료 등록하기"):
    if name.strip():
        st.session_state.inventory.append({"name": name.strip(), "expiry": expiry_date})
        st.success(f"✅ '{name}' (유통기한: {expiry_date}) 등록 완료!")
    else:
        st.error("❌ 식재료 이름을 입력해 주세요.")

st.divider()

# 2. 유통기한 현황
st.header("2. 유통기한 현황")
if st.session_state.inventory:
    today = datetime.now().date()
    sorted_inv = sorted(st.session_state.inventory, key=lambda x: x["expiry"])
    
    for item in sorted_inv:
        d_day = (item["expiry"] - today).days
        if d_day < 0:
            st.error(f"⚠️ {item['name']} | 유통기한: {item['expiry']} ({abs(d_day)}일 경과)")
        elif d_day <= 3:
            st.warning(f"🚨 {item['name']} | 유통기한: {item['expiry']} (D-{d_day})")
        else:
            st.info(f"✅ {item['name']} | 유통기한: {item['expiry']} (D-{d_day})")
else:
    st.write("현재 등록된 식재료가 없습니다.")

st.divider()

# 3. 레시피 추천
st.header("3. 보유 재료 기반 추천 레시피")
if st.session_state.inventory:
    available = set(item["name"] for item in st.session_state.inventory)
    matched = False
    for recipe, required in recipes.items():
        has = set(required).intersection(available)
        if len(has) / len(required) >= 0.5:
            matched = True
            missing = set(required) - available
            st.write(f"👉 **{recipe}** (보유 중: {', '.join(has)})")
            if missing:
                st.caption(f"   └ 부족한 재료: {', '.join(missing)}")
    if not matched:
        st.write("조리 가능한 레시피가 없습니다.")
