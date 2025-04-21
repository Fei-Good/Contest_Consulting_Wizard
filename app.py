import streamlit as st
import requests
import time
import os

# 页面配置
st.set_page_config(
    page_title="赛讯精灵 - 竞赛智能客服机器人",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
    }
    .bot-message {
        background-color: #F9FAFB;
        border-left: 5px solid #10B981;
    }
    .send-button {
        background-color: #2563EB;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .sidebar-header {
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.markdown("<div class='sidebar-header'>赛讯精灵</div>", unsafe_allow_html=True)
    
    st.markdown("### 📄 文档管理")
    
    # 上传文档部分
    st.markdown("#### 上传竞赛文档")
    pdf_file = st.file_uploader("选择PDF文件", type=["pdf"])
    
    upload_button = st.button("上传文档")
    if upload_button and pdf_file:
        with st.spinner("文档上传中..."):
            response = requests.post(
                "http://localhost:8000/upload_pdf",
                files={"file": (pdf_file.name, pdf_file, "application/pdf")},
            )
            if response.status_code == 200:
                st.success("✅ 文档上传成功")
            else:
                st.error("❌ 文档上传失败")
    
    # 文档列表
    st.markdown("#### 已上传文档")
    if os.path.exists("pdf"):
        pdf_files = [f for f in os.listdir("pdf") if f.endswith('.pdf')]
        if pdf_files:
            for pdf in pdf_files:
                st.text(f"• {pdf}")
        else:
            st.text("暂无文档")
    
    # 系统信息
    st.markdown("---")
    st.markdown("<div class='info-box'>赛讯精灵是一款专为竞赛咨询设计的智能客服机器人，可以回答有关竞赛规则、流程、评分标准等问题。</div>", unsafe_allow_html=True)
    st.markdown("版本: v1.0.0")

# 主界面
st.markdown("<h1 class='main-header'>🤖 赛讯精灵</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>竞赛智能客服机器人 - 您的竞赛咨询专家</p>", unsafe_allow_html=True)

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-message user-message'><b>👤 您:</b> {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message bot-message'><b>🤖 赛讯精灵:</b> {message['content']}</div>", unsafe_allow_html=True)

# 用户输入区域
st.markdown("### 💬 输入您的问题")
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("", placeholder="例如：这个竞赛的报名截止日期是什么时候？", key="user_input")
with col2:
    send_button = st.button("发送", use_container_width=True)

# 处理用户输入
if send_button and user_input:
    # 添加用户消息到聊天记录
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 显示最新的用户消息
    st.markdown(f"<div class='chat-message user-message'><b>👤 您:</b> {user_input}</div>", unsafe_allow_html=True)
    
    # 显示机器人思考中
    with st.spinner("思考中..."):
        try:
            res = requests.post("http://localhost:8000/chat", data={"query": user_input})
            if res.status_code == 200:
                response = res.json()["response"]
                # 添加机器人回复到聊天记录
                st.session_state.messages.append({"role": "assistant", "content": response})
                # 显示最新的机器人回复
                st.markdown(f"<div class='chat-message bot-message'><b>🤖 赛讯精灵:</b> {response}</div>", unsafe_allow_html=True)
            else:
                st.error("请求失败，请稍后再试")
        except Exception as e:
            st.error(f"发生错误: {str(e)}")
    
    # 清空输入框
    st.rerun()

# 常见问题示例
st.markdown("---")
st.markdown("### 📌 常见问题")

col1, col2 = st.columns(2)
with col1:
    if st.button("如何报名参加竞赛？", key="q1"):
        st.session_state.messages.append({"role": "user", "content": "如何报名参加竞赛？"})
        st.rerun()
    if st.button("竞赛评分标准是什么？", key="q2"):
        st.session_state.messages.append({"role": "user", "content": "竞赛评分标准是什么？"})
        st.rerun()
with col2:
    if st.button("竞赛的奖项设置有哪些？", key="q3"):
        st.session_state.messages.append({"role": "user", "content": "竞赛的奖项设置有哪些？"})
        st.rerun()
    if st.button("材料提交的截止日期是？", key="q4"):
        st.session_state.messages.append({"role": "user", "content": "材料提交的截止日期是？"})
        st.rerun()

# 页脚
st.markdown("---")
st.markdown("<div style='text-align: center; color: #6B7280; font-size: 0.8rem;'>© 2024 赛讯精灵 - 竞赛智能客服机器人 | 技术支持：AI团队</div>", unsafe_allow_html=True)
