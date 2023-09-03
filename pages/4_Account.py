import streamlit as st
import account

account.sign_up("사장님")

if st.session_state.signedout:
    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        # st.session_state.username = ""
        st.session_state.useremail = ""


    if st.session_state.signout:
        st.title("사용자 정보")
        st.text(st.session_state.useremail)
        st.button("나가기", on_click=t)