import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
# from semantha_streamlit_compare.components.compare import SemanticCompare
import os
import streamlit_authenticator as stauth

def main():
    st.set_page_config(layout="wide")
    st.title("CONDUCTOR")
    st.markdown("""---""")
    col1, col2 = st.columns(2)

    with col1:
        # st.button("사장님으로 시작하기", type="primary", page="2_CEO")
        st.markdown('<a href="/CEO" style="color: white; background-color: #04AA6D; border: none; padding: 20px; border-radius: 10px;" target="_self">사장님으로 시작하기</a>', unsafe_allow_html=True)

    with col2:
        st.markdown('<a href="/Trainee" style="color: white; background-color: orange; border: none; padding: 20px; border-radius: 10px;" target="_self">직원으로 학습하기</a>', unsafe_allow_html=True)
        # st.button("직원으로 학습하기",type="primary", page="3_Trainee")

    st.markdown("""---""")

    st.subheader("사장님은 다른일 하기 바쁘니까")
    st.text("사장님이 직원교육을 하지 마세요. CONDUCTOR가 해드릴께요.")

    st.subheader("필요성")
    st.image("https://firebasestorage.googleapis.com/v0/b/conductor-7ee1a.appspot.com/o/require.png?alt=media&token=142949c9-54a1-4fa1-8e9c-efe4c7c49a83", width=800)
    st.text("""소상공인들이 하기 싫은 일 1위로 직원관리 업무라는 결과가 나왔다(2020.02.20.,한국 M&A경제신문).\n직원들을 채용하고 교육하는 과정은 금전적 비용과 시간을 많이 소요하기 때문에, 직원관리 업무의 부담을 줄여주는 방안이 필요하다.""")

    st.subheader("제안 아이디어")
    st.image("https://firebasestorage.googleapis.com/v0/b/conductor-7ee1a.appspot.com/o/idea.png?alt=media&token=be48bbe5-134e-46ad-9646-f9445430207f", width=800)
    st.text(
        """기존에 사람이 직접 기록, 정리, 전달하는 정보 전달 방식을 인공지능의 도움으로 쉽고 명확하게 정리해주는 시스템을\n중소기업, 소상공인 사장님들이 쉽게 활용할 수 있는 서비스로 제안""")

    st.subheader("개발 현황")
    st.image("https://firebasestorage.googleapis.com/v0/b/conductor-7ee1a.appspot.com/o/service.png?alt=media&token=de0b8995-bf40-442f-ac12-4bc47e1d3cb0", width=800)
    st.text("""   - 현재 개발 단계에서는 직원 교육에 기능 집중하여 MVP 구현
 (MVP: ①사장님이 자료 파일을 서비스 업로드 하면, ②직원용 교육 프로그램을 만들어 주고, ③교육까지 도와주는 서비스) 
- 향후 프리랜서 활용한 교육자료의 디자인 개선 등 서비스 확장 예정
""")
    st.subheader("시간 없는 사장님들을 위한 서비스 CONDUCTOR")
    st.subheader("Contact")
    st.text("기획/개발자: 남윤덕, 전지훈")
    st.text("이메일: youndukn1@gmail.com")

main()