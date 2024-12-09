import streamlit as st
import pages/2_Mock_Interview.py
import openai
from openai import OpenAIError

# Streamlit 기본 설정
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("💼 면접 준비 팁 제공")

# OpenAI API Key 입력
api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
if api_key:
    openai.api_key = api_key
    st.session_state["api_key"] = api_key
else:
    st.warning("OpenAI API Key를 입력하세요.")
    st.stop()

# 면접 기록 불러오기
if "interview_messages" not in st.session_state or not st.session_state["interview_messages"]:
    st.warning("면접 기록이 없습니다. 면접 기록을 먼저 생성해주세요.")
    st.stop()

# 면접 준비 팁 생성 함수
@st.cache_data
def generate_tips_with_interview(job_title, interview_content):
    messages = [
        {"role": "system", "content": "You are an expert interview coach. Please respond in Korean."},
        {
            "role": "user",
            "content": f"""
            사용자의 면접 기록과 직업명 "{job_title}"을 참고하여 면접 준비 팁을 작성해주세요.
            면접 기록:
            {interview_content}
            
            작성 항목:
            1. 면접 기록에 기반한 사용자 피드백
            2. "{job_title}" 직업에 특화된 맞춤형 면접 준비 팁
            각각의 항목을 명확히 구분하여 작성해주세요."""
        }
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        content = response["choices"][0]["message"]["content"]
        # 문장이 중간에 끊기지 않도록 처리
        if not content.endswith(("다.", "요.", "습니다.", "습니까?", "에요.")):
            content = content.rsplit('.', 1)[0] + '.'
        return content
    except OpenAIError as e:
        return f"OpenAI API 오류 발생: {e}"

# 면접 기록과 직업명 입력
st.write("### 면접 준비 팁 생성")
job_title = st.text_input("직업명을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")
interview_content = "\n".join(
    [f"{msg['role']}: {msg['content']}" for msg in st.session_state["interview_messages"]]
)

if st.button("면접 준비 팁 생성"):
    if not job_title:
        st.warning("직업명을 입력해주세요.")
    else:
        with st.spinner("면접 준비 팁을 생성 중입니다..."):
            tips = generate_tips_with_interview(job_title, interview_content)
        st.success(f'"{job_title}" 직업에 대한 면접 준비 팁이 생성되었습니다!')
        st.write(tips)
