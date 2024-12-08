import streamlit as st
import openai

# Streamlit 페이지 구성
st.title("AI 기반 면접 코칭 사이트")
st.write("OpenAI API를 활용해 원하는 직업에 맞는 면접 팁과 정보를 제공합니다.")

# OpenAI API Key 입력
api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

# 원하는 직업 입력
job_title = st.text_input("원하는 직업을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

# API Key 확인
if not api_key:
    st.warning("OpenAI API 키를 입력하세요.")
else:
    openai.api_key = api_key

# OpenAI API를 통해 면접 정보 생성
if st.button("면접 준비 자료 생성"):
    if not job_title:
        st.warning("직업명을 입력하세요.")
    else:
        try:
            with st.spinner("AI가 면접 팁을 준비 중입니다..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional interview coach."},
                        {"role": "user", "content": f"Provide detailed interview tips and preparation materials for the job of {job_title}."},
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                tips = response['choices'][0]['message']['content']
                st.success("면접 준비 자료가 생성되었습니다!")
                st.write(f"### {job_title} 직업에 대한 면접 팁")
                st.write(tips)
        except openai.error.OpenAIError as e:  # 모든 OpenAI 오류를 처리
            st.error(f"OpenAI API 오류: {str(e)}")
        except Exception as e:  # 기타 오류를 처리
            st.error(f"오류가 발생했습니다: {str(e)}")
