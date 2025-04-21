from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config.templates import QA_PROMPT
from models.embedding_model import get_embedding_model
from models.llm_model import get_llm
from utils.utils import (
    extract_text_from_PDF,
    split_content_into_chunks,
    save_chunks_into_vectorstore,
    get_chat_chain,
    process_user_input
)
import os

class ChatBot:
    def __init__(self):
        self.vector_store = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.embedding_model = get_embedding_model()
        self.llm = get_llm()
        self.qa_chain = None



    def load_pdf(self, file_path: str):
        if not os.path.exists(file_path):
            return "❌ 文件不存在"
        try:
            text = extract_text_from_PDF(file_path)
            chunks = split_content_into_chunks(text)
            self.vector_store = save_chunks_into_vectorstore(chunks, self.embedding_model)
            self.qa_chain = get_chat_chain(self.llm, self.vector_store, self.memory)
            self.memory.clear()  # 清空历史对话
            return "✅ 文档加载完成"
        except Exception as e:
            return f"❌ 文档处理出错: {str(e)}"

    def ask(self, query: str):
        if not self.qa_chain:
            return "⚠️ 请先上传文档。"
        try:
            return process_user_input(self.qa_chain, query)
        except Exception as e:
            return f"⚠️ 回答生成出错: {str(e)}"