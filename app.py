import streamlit as st
import random
import time

# 1. 애플리케이션 제목
st.title("사다리 타기")

# 2. 사다리 개수 입력
num_items = st.number_input("사다리 항목 개수를 입력하세요 (2~10)", min_value=2, max_value=10, step=1)

if num_items:
    # 3. 항목 이름 입력
    st.subheader("항목 이름을 입력하세요")
    items = []
    for i in range(1, int(num_items) + 1):
        item_name = st.text_input(f"{i}번 항목 이름", key=f"item_{i}")
        if item_name:
            items.append(item_name)

    if len(items) == num_items:
        st.success("모든 항목 이름이 입력되었습니다. 사다리타기를 시작하세요!")

        # 4. 사다리 결과 매칭 (랜덤 결과)
        results = random.sample(items, len(items))
        if st.button("사다리 타기 결과 보기"):
            # 사다리 애니메이션 출력
            st.subheader("사다리타기 진행 중...")
            ladder_progress = [f"{i}번 → 결과로 이동 중..." for i in range(1, len(items)+1)]
            for step in ladder_progress:
                st.write(step)
                time.sleep(0.5)

            # 5. 결과 표시
            st.subheader("사다리 결과")
            for idx, result in enumerate(results):
                st.write(f"{items[idx]} → {result}")
