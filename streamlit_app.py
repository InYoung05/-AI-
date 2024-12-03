import openai
import streamlit as st

# OpenAI API Key 설정
openai.api_key = 'your-openai-api-key'

# 면접 팁 요청 함수
def get_interview_tips(job_title):
    prompt = f"면접 준비를 위한 유용한 팁을 제공해주세요. 직업: {job_title}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

# 직업 관련 자격증 정보 요청 함수
def get_certifications(job_title):
    prompt = f"{job_title}에 필요한 자격증과 관련 정보를 알려주세요."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

# Streamlit 페이지 구성
def main():
    st.title("AI 기반 면접 준비 코칭 사이트")
    
    # 직업 선택
    job_title = st.text_input("면접을 준비할 직업을 입력하세요 (예: 소프트웨어 개발자, 마케팅 매니저 등):")
    
    if job_title:
        st.subheader(f"{job_title} 면접 준비 팁")
        interview_tips = get_interview_tips(job_title)
        st.write(interview_tips)
        
        st.subheader(f"{job_title} 관련 자격증 정보")
        certifications = get_certifications(job_title)
        st.write(certifications)
//////////////////
import openai
import streamlit as st

# OpenAI API 키 설정
openai.api_key = "YOUR_OPENAI_API_KEY"  # 본인의 OpenAI API 키를 여기에 입력하세요.

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
                model="gpt-4",
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
