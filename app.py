import streamlit as st
import random
import time

# 참여자와 소지품 입력
st.title("사다리 타기 이벤트")
participants = st.text_area("참여자 이름을 입력하세요 (쉼표로 구분)", placeholder="예: 홍길동, 이순신, 강감찬")
items = st.text_area("소지품을 입력하세요 (쉼표로 구분)", placeholder="예: 숟가락, 젓가락, 컵")

if st.button("사다리 생성"):
    # 입력 데이터를 처리
    names = [name.strip() for name in participants.split(",") if name.strip()]
    item_list = [item.strip() for item in items.split(",") if item.strip()]
    
    if len(names) != len(item_list):
        st.error("참여자 수와 소지품 수가 같아야 합니다!")
    else:
        # 랜덤 매칭 생성
        random.shuffle(item_list)
        result = dict(zip(names, item_list))
        
        # 사다리 표시
        st.write("### 사다리 생성 중...")
        time.sleep(1)
        
        # 결과 출력
        for name in names:
            st.write(f"{name} -> {result[name]}")
            time.sleep(1)
