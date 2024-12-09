import streamlit as st
import openai

# Streamlit 페이지 구성
st.title("AI 기반 면접 코칭 사이트")
st.write("OpenAI API를 활용해 원하는 직업에 맞는 면접 팁과 정보를 제공합니다.")

# OpenAI API Key 입력
api_key = st.text_input("OpenAI API Key", 
                        value=st.session_state.get('api_key', ''), 
                        type='password')

# API Key 확인 후 세션 상태에 저장
if api_key:
    st.session_state['api_key'] = api_key
    if 'openai_client' not in st.session_state:
        openai.api_key = api_key  # API 키 설정
        st.session_state['openai_client'] = openai  # OpenAI 클라이언트 세션에 저장

# 원하는 직업 입력
job_title = st.text_input("원하는 직업을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

# 면접 대화 기록 세션에 저장
if 'interview_history' not in st.session_state:
    st.session_state['interview_history'] = []  # 초기화

# OpenAI API를 통해 면접 정보 생성
@st.cache_data
def get_interview_tips(job_title, history):
    # OpenAI API 호출
    if 'openai_client' in st.session_state:
        openai_client = st.session_state['openai_client']
        
        # 대화 기록과 새로운 요청을 포함하여 API 호출
        messages = [{"role": "system", "content": "You are a professional interview coach. Please respond in Korean."}]
        messages.extend(history)  # 대화 기록 추가
        messages.append({"role": "user", "content": f"Provide detailed interview tips and preparation materials for the job of {job_title}."})
        
        # ChatCompletion.create 방식으로 호출
        response = openai_client.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 최신 모델 사용
            messages=messages,  # 메시지 형식으로 시스템 및 사용자 입력 설정
            max_tokens=500,
            temperature=0.7,
        )
        return response['choices'][0]['message']['content'].strip()  # 응답에서 텍스트만 추출
    else:
        return "OpenAI 클라이언트가 초기화되지 않았습니다."

if st.button("면접 준비 자료 생성"):
    if not job_title:
        st.warning("직업명을 입력하세요.")
    elif not api_key:
        st.warning("OpenAI API 키를 입력하세요.")
    else:
        try:
            with st.spinner("AI가 면접 팁을 준비 중입니다..."):
                tips = get_interview_tips(job_title, st.session_state['interview_history'])
                
                # 대화 기록 업데이트
                st.session_state['interview_history'].append(
                    {"role": "user", "content": f"Provide detailed interview tips and preparation materials for the job of {job_title}."}
                )
                st.session_state['interview_history'].append(
                    {"role": "assistant", "content": tips}
                )

                st.success("면접 준비 자료가 생성되었습니다!")
                st.write(f"### {job_title} 직업에 대한 면접 팁")
                st.write(tips)

        except openai.OpenAIError as e:
            st.error(f"OpenAI API 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

# 이전 면접 대화 보기
if st.checkbox("면접 대화 기록 보기"):
    st.write("### 면접 대화 기록")
    for record in st.session_state['interview_history']:
        if record['role'] == 'user':
            st.write(f"**사용자:** {record['content']}")
        elif record['role'] == 'assistant':
            st.write(f"**AI:** {record['content']}")
/////////////////////////////
import streamlit as st
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
            max_tokens=500,
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
