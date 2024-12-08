import openai
import streamlit as st

# API Key 입력
api_key = st.text_input("OpenAI API Key", 
                        value=st.session_state.get('api_key',''),
                        type='password')

# API 키를 세션 상태에 저장하고 OpenAI 클라이언트 생성
if api_key:
    st.session_state['api_key'] = api_key
    if 'openai_client' in st.session_state:
        # 기존 OpenAI 클라이언트가 있다면 그대로 사용
        client = st.session_state['openai_client']
    else:
        # 새로 OpenAI 클라이언트 생성
        client = openai
        st.session_state['openai_client'] = client

# API Key 확인
if not api_key:
    st.warning("OpenAI API 키를 입력하세요.")
else:
    openai.api_key = api_key  # OpenAI API 키 설정

# 면접 팁을 가져오는 함수 정의
@st.cache_data
def get_interview_tips(job_title):
    # OpenAI API 호출
    return response['choices'][0]['message']['content']

# 원하는 직업 입력
job_title = st.text_input("원하는 직업을 입력하세요 (예: 데이터 분석가, 소프트웨어 엔지니어)")

# 면접 준비 자료 생성 버튼 클릭
if st.button("면접 준비 자료 생성"):
    if not job_title:
        st.warning("직업명을 입력하세요.")
    else:
        try:
            with st.spinner("AI가 면접 팁을 준비 중입니다..."):
                # OpenAI API 호출 (ChatCompletion 사용)
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # 최신 모델을 사용하세요
                    messages=[
                        {"role": "system", "content": "You are a professional interview coach. Please respond in Korean."},
                        {"role": "user", "content": f"Provide detailed interview tips and preparation materials for the job of {job_title}."}
                    ],
                    max_tokens=500,
                    temperature=0.7,
                )
                
                tips = response['choices'][0]['message']['content']

                # 글자가 초과하는 경우 마지막 문장까지 자르기 (숫자와 공백 포함)
                def truncate_text(text):
                    sentences = text.split('. ')
                    if len(sentences) > 1:
                        text_to_return = '. '.join(sentences[:-1]) + '.'
                        if text_to_return[-1].isdigit():
                            text_to_return = '. '.join(sentences[:-2]) + '.'
                        text_to_return = text_to_return.rstrip('0123456789. ') 
                        return text_to_return
                    return text

                tips = truncate_text(tips).strip()

                st.success("면접 준비 자료가 생성되었습니다!")
                st.write(f"### {job_title} 직업에 대한 면접 팁")
                st.write(tips)

        except openai.OpenAIError as e:
            st.error(f"OpenAI API 오류가 발생했습니다: {str(e)}")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
