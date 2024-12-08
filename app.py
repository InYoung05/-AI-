import streamlit as st
import openai

# Streamlit 페이지 구성
st.title("AI 기반 면접 코칭 사이트")
st.write("OpenAI API를 활용해 원하는 직업에 맞는 면접 팁과 정보를 제공합니다.")

# OpenAI API Key 입력
api_key = st.text_input("OpenAI API Key", 
                        value=st.session_state.get('api_key', ''),
                        type='password')

if api_key:
    st.session_state['api_key'] = api_key
    openai.api_key = api_key

# 원하는 직업 입력
job_title = st.text_input("원하는 직업을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

@st.cache_data
def get_interview_tips(job_title):
    # OpenAI API 호출 (최신 버전 메서드 사용)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional interview coach. Please respond in Korean."},
            {"role": "user", "content": f"Provide detailed interview tips and preparation materials for the job of {job_title}."},
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content']

# OpenAI API를 통해 면접 정보 생성
if st.button("면접 준비 자료 생성"):
    if not job_title:
        st.warning("직업명을 입력하세요.")
    else:
        try:
            with st.spinner("AI가 면접 팁을 준비 중입니다..."):
                tips = get_interview_tips(job_title)
                st.success("면접 준비 자료가 생성되었습니다!")
                st.write(f"### {job_title} 직업에 대한 면접 팁")
                st.write(tips)

        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
