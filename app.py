import streamlit as st
import openai
from openai import OpenAIError

# Streamlit 기본 설정
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("💼 면접 준비 팁 제공")

# OpenAI API Key 가져오면 없앨 입력 코드
api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.get("api_key", ""))
if api_key:
    openai.api_key = api_key
    st.session_state["api_key"] = api_key
else:
    st.warning("OpenAI API Key를 입력하세요.")
    st.stop()

# 면접 기록 확인
if "interview_messages" not in st.session_state or not st.session_state["interview_messages"]:
    st.warning("면접 기록이 없습니다. 먼저 모의 면접을 진행해주세요.")

# 면접 기록 불러오기
if "interview_messages" in st.session_state and st.session_state["interview_messages"]:
    st.write("### 면접 기록")
    for msg in st.session_state["interview_messages"]:
        role = "👤 사용자" if msg["role"] == "user" else "🤖 면접관"
        st.write(f"{role}: {msg['content']}")

# 면접 준비 팁 생성 함수
@st.cache_data
def generate_tips_with_interview(job_title, interview_content=None):
    if interview_content:
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
                각각의 항목을 명확히 구분하여 작성해주세요."""}
        ]
    else:
        messages = [
            {"role": "system", "content": "You are an expert interview coach. Please respond in Korean."},
            {
                "role": "user",
                "content": f"""
                "{job_title}" 직업에 특화된 면접 준비 팁을 작성해주세요.
                
                작성 항목:
                1. "{job_title}" 직업에 맞는 면접 준비 팁
                """
            }
        ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        content = response["choices"][0]["message"]["content"]
        # 문장이 중간에 끊기지 않도록 처리
        if not content.endswith(("다.", "요.", "습니다.", "습니까?", "에요.")):
            content = content.rsplit('.', 1)[0] + '.'
        
        # 마지막 항목이 완전하게 마무리된 형태로 만들기
        if content.endswith(('.', '요.', '습니다.', '에요.')):
            return content
        else:
            content = content.rstrip()
            if content:
                content += '.'
            return content
    except OpenAIError as e:
        return f"OpenAI API 오류 발생: {e}"

# 직업명 입력과 팁 생성
st.write("### 면접 준비 팁 생성")
job_title = st.text_input("직업명을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

interview_content = "\n".join(
    [f"{msg['role']}: {msg['content']}" for msg in st.session_state["interview_messages"]]
) if "interview_messages" in st.session_state else None

if st.button("면접 준비 팁 생성"):
    if not job_title:
        st.warning("직업명을 입력해주세요.")
    else:
        with st.spinner("면접 준비 팁을 생성 중입니다..."):
            tips = generate_tips_with_interview(job_title, interview_content)
        st.success(f'"{job_title}" 직업에 대한 면접 준비 팁이 생성되었습니다!')
        st.write(tips)
