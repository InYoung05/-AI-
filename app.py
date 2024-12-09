import streamlit as st
import openai
import json

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
    openai.api_key = api_key  # OpenAI API 키 설정

# 면접 기록 관리
if 'interview_history' not in st.session_state:
    st.session_state['interview_history'] = []  # 초기화

# 면접 기록 파일 업로드 기능
st.write("## 면접 기록 파일 업로드")
uploaded_file = st.file_uploader("면접 기록 파일을 업로드하세요 (.txt 또는 .json)", type=["txt", "json"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.json'):
            interview_data = json.load(uploaded_file)
            st.session_state['interview_history'] = interview_data
        elif uploaded_file.name.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
            st.session_state['interview_history'] = [{"role": "user", "content": line} for line in content.splitlines()]
        st.success("면접 기록이 업로드되었습니다!")
    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {str(e)}")

# OpenAI를 통해 면접 준비 정보 생성
@st.cache_data
def generate_preparation_tips(job_title, history):
    messages = [
        {"role": "system", "content": "You are an expert interview coach. Please respond in Korean."},
        {"role": "user", "content": f"사용자의 과거 면접 기록: {history}. 이 기록을 참고하여 {job_title} 직업에 대한 맞춤형 면접 준비 팁을 제공하세요."},
        {"role": "user", "content": f"그리고 일반적으로 {job_title} 직업에 필요한 면접 준비 팁도 추가로 제공해주세요."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    
    # 응답 텍스트 추출
    content = response['choices'][0]['message']['content'].strip()
    
    # 문장이 중간에 끊기지 않도록 처리
    if not content.endswith(("다.", "요.", "습니다.", "습니까?", "에요.")):
        content = content.rsplit('.', 1)[0] + '.'
    
    return content

# 새로운 면접 준비
st.write("## 면접 준비")
job_title = st.text_input("원하는 직업을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

if st.button("면접 준비 정보 생성"):
    if not job_title:
        st.warning("직업명을 입력하세요.")
    elif not api_key:
        st.warning("OpenAI API 키를 입력하세요.")
    else:
        try:
            # 면접 기록 기반으로 정보 생성
            history_text = "\n".join([f"{record['role'].capitalize()}: {record['content']}" for record in st.session_state['interview_history']])
            with st.spinner("AI가 면접 준비 정보를 생성 중입니다..."):
                tips = generate_preparation_tips(job_title, history_text)
                
                # 대화 기록 업데이트
                st.session_state['interview_history'].append(
                    {"role": "user", "content": f"Provide preparation tips for {job_title} based on past interviews and general guidelines."}
                )
                st.session_state['interview_history'].append(
                    {"role": "assistant", "content": tips}
                )

                # 준비 정보 표시
                st.success("면접 준비 정보가 생성되었습니다!")
                st.write(f"### {job_title} 직업에 대한 면접 준비 팁")
                st.write(tips)
        except openai.error.OpenAIError as e:
            st.error(f"OpenAI API 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

# 면접 기록 보기
st.write("## 면접 대화 기록")
if st.session_state['interview_history']:
    for record in st.session_state['interview_history']:
        if record['role'] == 'user':
            st.write(f"**사용자:** {record['content']}")
        elif record['role'] == 'assistant':
            st.write(f"**AI:** {record['content']}")
else:
    st.info("면접 기록이 없습니다.")
