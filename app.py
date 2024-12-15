import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow

# 사다리 생성 함수
def generate_ladder(num_items, num_steps=5):
    """사다리를 생성하고 가로줄 위치를 반환"""
    ladder = [[False] * (num_steps + 1) for _ in range(num_items)]
    for step in range(num_steps):
        for col in range(num_items - 1):
            if random.choice([True, False]):  # 무작위로 가로줄 생성
                ladder[col][step] = True
    return ladder

# 사다리 시각화 함수
def draw_ladder(ladder, current_position=None):
    """사다리를 시각화하고 현재 위치를 표시"""
    num_items = len(ladder)
    num_steps = len(ladder[0])
    plt.figure(figsize=(8, 6))
    for col in range(num_items):
        plt.plot([col, col], [0, num_steps], color="black", linewidth=2)  # 세로줄

    # 가로줄
    for col in range(num_items - 1):
        for step in range(num_steps):
            if ladder[col][step]:
                plt.plot([col, col + 1], [step, step], color="blue", linewidth=2)

    # 현재 위치 표시
    if current_position:
        plt.scatter(
            current_position[0], current_position[1], color="red", s=100, label="현재 위치"
        )

    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.legend()
    st.pyplot(plt.gcf())
    plt.close()

# 사다리 애니메이션 함수
def run_ladder(ladder, start_col):
    """사다리 애니메이션을 실행하며 경로를 반환"""
    num_steps = len(ladder[0])
    current_col = start_col
    path = [(current_col, 0)]  # 시작점

    for step in range(num_steps):
        # 아래로 이동
        path.append((current_col, step + 1))
        # 좌우 이동 여부 결정
        if current_col > 0 and ladder[current_col - 1][step]:
            current_col -= 1  # 왼쪽 이동
            path.append((current_col, step + 1))
        elif current_col < len(ladder) - 1 and ladder[current_col][step]:
            current_col += 1  # 오른쪽 이동
            path.append((current_col, step + 1))

    return path

# Streamlit 인터페이스
st.title("네이버 스타일 사다리타기")
num_items = st.number_input("항목 개수를 입력하세요 (2~10)", min_value=2, max_value=10, step=1)

if num_items:
    items = []
    st.subheader("항목 이름 입력")
    for i in range(1, num_items + 1):
        item_name = st.text_input(f"{i}번 항목 이름", key=f"item_{i}")
        if item_name:
            items.append(item_name)

    if len(items) == num_items:
        st.success("모든 항목 이름이 입력되었습니다. 사다리를 생성합니다.")

        if st.button("사다리 생성"):
            # 사다리 생성
            ladder = generate_ladder(num_items)
            draw_ladder(ladder)  # 초기 사다리 표시

            st.info("아래 항목을 클릭하여 사다리타기를 시작하세요!")
            for idx, item in enumerate(items):
                if st.button(f"{item} 시작"):
                    st.write(f"{item}의 사다리타기 진행 중...")
                    path = run_ladder(ladder, idx)

                    # 애니메이션 표시
                    for position in path:
                        draw_ladder(ladder, position)
                        time.sleep(0.5)

                    # 결과 표시
                    result = random.choice(items)
                    st.success(f"결과: {item} → {result}")
