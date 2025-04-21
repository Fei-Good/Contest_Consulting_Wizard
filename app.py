import streamlit as st
import requests

st.title("📘 竞赛问答助手 ChatBot")

with st.sidebar:
    st.header("上传竞赛文档")
    pdf_file = st.file_uploader("上传 PDF 文件", type=["pdf"])
    if pdf_file:
        response = requests.post(
            "http://localhost:8000/upload_pdf",
            files={"file": (pdf_file.name, pdf_file, "application/pdf")},
        )
        st.success("文档上传成功")

st.markdown("输入你的问题：")
user_input = st.text_input("", key="user_input")

if st.button("发送") and user_input:
    res = requests.post("http://localhost:8000/chat", data={"query": user_input})
    st.write("🤖: ", res.json()["response"])
