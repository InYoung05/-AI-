import openai
import streamlit as st

# OpenAI API 키 설정
openai.api_key = "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"  # 본인의 OpenAI API 키를 여기에 입력하세요.

# Streamlit 페이지 구성
st.title("AI 기반 면접 준비 코칭 사이트")
st.header("면접 준비를 AI와 함께!")

# 사용자가 입력한 직업군
job = st.text_input("원하는 직업을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

if job:
    # OpenAI API를 사용하여 자격증 및 면접 팁 가져오기
    with st.spinner("AI가 정보를 가져오고 있습니다..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4 mini",
                messages=[
                    {"role": "system", "content": "당신은 면접 준비 코치입니다."},
                    {"role": "user", "content": f"{job} 직업에 필요한 주요 자격증과 면접 준비 팁을 알려주세요."}
                ],
                max_tokens=500,
                temperature=0.7,
            )

            # AI의 응답 출력
            result = response['choices'][0]['message']['content']
            st.success("정보를 성공적으로 가져왔습니다!")
            st.subheader(f"{job} 직업 관련 정보")
            st.text_area("AI가 추천하는 자격증 및 면접 팁", value=result, height=300)
        
        except Exception as e:
            st.error("정보를 가져오는 중 오류가 발생했습니다. 다시 시도해주세요.")
            st.write(e)

# 부가적인 면접 준비 팁 섹션
st.sidebar.title("부가 정보")
st.sidebar.info("자신감 있는 태도, 명확한 의사소통, 관련 프로젝트 경험 공유 등도 중요합니다!")
st.sidebar.text("📌 팁: 모의 면접을 통해 실전 감각을 익히세요!")
