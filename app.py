import streamlit as st
import random
import time
import matplotlib.pyplot as plt

# 사다리 생성 함수
def generate_ladder(num_items, num_steps=6):
    """사다리를 생성하고 가로줄 위치를 반환"""
    ladder = [[False] * num_steps for _ in range(num_items)]
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

    # 세로줄
    for col in range(num_items):
        plt.plot([col, col], [0, num_steps], color="black", linewidth=2)

    # 가로줄
    for col in range(num_items - 1):
        for step in range(num_steps):
            if ladder[col][step]:
                plt.plot([col, col + 1], [step, step], color="blue", linewidth=2)

    # 현재 위치 표시
    if current_position:
        x, y = current_position
        plt.scatter(x, y, color="red", s=100, zorder=5, label="현재 위치")

    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.legend(loc="upper right")
    st.pyplot(plt.gcf())
    plt.close()

# 사다리 애니메이션 함수
def run_ladder_animation(ladder, start_col):
    """선택된 항목에서 출발하여 사다리를 내려가는 모션 애니메이션"""
    num_steps = len(ladder[0])
    current_col = start_col
    x, y = current_col, 0  # 초기 위치
    path = [(x, y)]

    for step in range(num_steps):
        # 아래로 이동
        y += 1
        path.append((x, y))

        # 좌우 이동 여부 결정
        if x > 0 and ladder[x - 1][step]:
            x -= 1  # 왼쪽 이동
            path.append((x, y))
        elif x < len(ladder) - 1 and ladder[x][step]:
            x += 1  # 오른쪽 이동
            path.append((x, y))

    # 경로 애니메이션 표시
    for position in path:
        draw_ladder(ladder, position)
        time.sleep(0.5)

    return x  # 최종 도착 위치

# Streamlit 앱 구성
st.title("사다리 타기 - 점이 선을 따라 흐르는 모션")

# 항목 개수 입력
num_items = st.number_input("항목 개수를 입력하세요 (2~10)", min_value=2, max_value=10, step=1)

if num_items:
    st.subheader("항목 이름 입력")
    items = []
    for i in range(1, num_items + 1):
        item_name = st.text_input(f"{i}번 항목 이름", key=f"item_{i}")
        if item_name:
            items.append(item_name)

    if len(items) == num_items:
        st.success("모든 항목 이름이 입력되었습니다.")

        # 랜덤 결과 생성
        results = random.sample(items, len(items))

        # 사다리 생성
        ladder = generate_ladder(num_items)
        st.subheader("사다리 생성 완료")
        draw_ladder(ladder)  # 초기 사다리 표시

        st.subheader("사다리타기 진행")
        for idx, item in enumerate(items):
            col_button = st.button(item, key=f"button_{idx}")
            if col_button:
                st.info(f"{item}의 사다리타기 진행 중...")

                # 애니메이션 실행
                final_position = run_ladder_animation(ladder, idx)

                # 결과 표시
                st.success(f"결과: {item} → {results[final_position]}")
                break
