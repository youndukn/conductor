import streamlit as st
import streamlit_authenticator as stauth
import datetime

import re

import firebase_admin

from firebase_admin import credentials
from firebase_admin import auth
import json

json_data = json.loads(st.secrets["google_json"], strict=False)

if not firebase_admin._apps:
    cred = credentials.Certificate(json_data)
    firebase_admin.initialize_app(cred)

def sign_up(role):

        if 'useremail' not in st.session_state:
            st.session_state.useremail = ''

        def f():
            try:
                user = auth.get_user_by_email(email)
                # print(user.uid)
                # st.success('로그인 성공')
                # st.session_state.username = user.uid
                st.session_state.useremail = user.email
                st.session_state.boss = user.display_name
                st.session_state.signedout = True
                st.session_state.signout = True

            except:
                st.warning('로그인 실패')
                st.session_state.signedout = False
                st.session_state.signout = False

        if 'signedout' not in st.session_state:
            st.session_state.signedout = False
        if 'signout' not in st.session_state:
            st.session_state.signout = False

        if not st.session_state.signedout:

            st.title("{}으로 로그인/가입하기".format(role))
            choice = st.selectbox('로그인/가입하기', ['로그인', '가입하기'])

            if choice == '로그인':
                st.subheader(":green[로그인]")
                email = st.text_input("이메일", placeholder="이메일로 로그인하기")
                password1 = st.text_input("비밀번호", placeholder="비밀번호", type="password")
                st.button('로그인', on_click=f)

            else:
                st.subheader(":green[가입하기]")
                email = st.text_input("이메일", placeholder="이메일을 넣어주세요")
                boss = st.text_input("사장님 이메일", placeholder="사장님 이메일을 넣어주세요")
                password1 = st.text_input("비밀번호", placeholder="비밀번호를 넣어주세요", type="password")
                password2 = st.text_input("비밀번호 재확인", placeholder="비밀번호 재확인해주세요", type="password")

                if st.button('가입하기'):
                    try:
                        user = auth.get_user_by_email(boss)
                        st.success('사장님 찾기 성공')
                    except:
                        st.error("사장님을 찾을수 없습니다.")

                    if password1 != password2:
                        st.error("비밀번호가 다릅니다.")
                    else:
                        try:

                            user = auth.create_user(email=email, password= password1, uid=email, display_name=boss)
                            if user:
                                # st.session_state.username = user.uid
                                st.session_state.useremail = user.email
                                st.session_state.signedout = True
                                st.session_state.signout = True
                                st.success("가입완료 하였습니다.")
                        except auth.UidAlreadyExistsError:
                            st.error("가입한 이메일입니다.")


