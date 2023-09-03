import streamlit as st
import account

import tempfile

from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma

import PyPDF2
import random
import itertools
import streamlit as st
from io import StringIO
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import SVMRetriever
from langchain.chains import QAGenerationChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from streamlit_calendar import calendar

import base64

import os

account.sign_up("직원")

openai_key = st.secrets["openai_key"]

question_list = ["오늘 숙지 해야되는 내용은 어떻게되?", ]

calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "building",
    "resources": [
        {"id": "a", "building": "Building A", "title": "Building A"},
        {"id": "b", "building": "Building A", "title": "Building B"},
        {"id": "c", "building": "Building B", "title": "Building C"},
        {"id": "d", "building": "Building B", "title": "Building D"},
        {"id": "e", "building": "Building C", "title": "Building E"},
        {"id": "f", "building": "Building C", "title": "Building F"},
    ],
}

def displayPDF(col, file):
    # Opening file from file path
    # with open(file, "rb") as f:
    base64_pdf = base64.b64encode(file).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = '<iframe src="data:application/pdf;base64,{}" width="700" height="1000" type="application/pdf"></iframe>'.format(base64_pdf)

    # Displaying File
    col.markdown(pdf_display, unsafe_allow_html=True)

def main():

    st.set_page_config(layout="wide")
    # st.set_page_config(page_title="Chat with multiple PDF", page_icon=":book:")
    if 'temp_filepath' not in st.session_state:
        st.title("안녕하세요 사장님! 직원 교육 자료를 넣어주세요")
        uploaded_file = st.file_uploader("PDF 파일을 올려주세요!", type=['pdf'])
        st.session_state.uploaded_file = uploaded_file

    def pdf_to_document(uploaded_file):
        temp_dir = tempfile.TemporaryDirectory()
        temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
        with open(temp_filepath, "wb") as f:
            f.write(uploaded_file.getvalue())
        loader = PyPDFLoader(temp_filepath)
        pages = loader.load_and_split()
        st.session_state.temp_filepath = temp_filepath
        return pages

    with st.sidebar:


        hobbies = st.multiselect("#HashTag:", [])

        # write the selected options
        # st.write("You selected", len(hobbies), 'hobbies')

    if "uploaded_file" in st.session_state:
        uploaded_file = st.session_state["uploaded_file"]
    else:
        uploaded_file = None

    if uploaded_file is not None:
        pages = pdf_to_document(uploaded_file)

        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=1000,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )

        embeddings_model = OpenAIEmbeddings(openai_api_key=openai_key)

        texts = text_splitter.split_documents(pages)

        db = Chroma.from_documents(texts, embeddings_model)

        from langchain.callbacks.base import BaseCallbackHandler
        class StreamHandler(BaseCallbackHandler):
            def __init__(self, container, initial_text=""):
                self.container = container
                self.text = initial_text

            def on_llm_new_token(self, token: str, **kwargs) -> None:
                self.text += token
                self.container.markdown(self.text)
                st.session_state.answer = self.text

        st.header("사장님께 질문 하고 싶은것이 있나요?")
        question2 = st.selectbox("미리 준비한 질문이 있어요 확인해보고 질문해 보세요.", question_list)
        st.text("또는 자유롭게 질문해 보세요.")
        question = st.text_input('질문을 입력하세요')
        col1, col2 = st.columns(2)

        if col1.button('질문하기'):
            with st.spinner('기다리는 중...'):
                chat_box = col1.empty()
                stream_hander = StreamHandler(chat_box)
                llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                                 temperature=0,
                                 openai_api_key=openai_key,
                                 streaming=True,
                                 callbacks=[stream_hander])
                qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
                if question == "":
                    question = question2
                qa_chain({"query": question})

        # col2.write(uploaded_file.upload_url)
        displayPDF(col2, st.session_state.uploaded_file.getvalue())

        if st.button("교육스케줄 확인하기"):
            st.session_state.schedule = True

        if "schedule" in st.session_state:
            if "answer" in st.session_state:
                st.markdown(st.session_state.answer)
            calendar1 = calendar(events=[], options=calendar_options)
            st.write(calendar1)

if st.session_state.signedout:
    main()
