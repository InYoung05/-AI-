import streamlit as st
import random

# 앱 제목
st.title("사다리 타기")

# 항목 입력 섹션
st.subheader("항목 입력")
items = st.text_area("각 항목을 줄바꿈으로 입력하세요 (예: 항목1, 항목2, 항목3)").split("\n")
items = [item.strip() for item in items if item.strip()]  # 빈 값 제거

# 결과 자동 생성 버튼
if st.button("사다리 생성"):
    if len(items) < 2:
        st.error("최소 두 개 이상의 항목을 입력해야 합니다!")
    else:
        # 사다리 결과 무작위 매칭
        results = random.sample(items, len(items))

        # 사다리 결과 매칭 표시
        st.subheader("결과 확인")
        for i, item in enumerate(items):
            st.write(f"**{item}** → {results[i]}")

        # 추가로 버튼을 누를 때마다 다른 매칭 결과를 볼 수도 있음
