from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

from chatbot import ChatBot
from langchain_community.vectorstores import FAISS

# 确保pdf目录存在
os.makedirs("pdf", exist_ok=True)

app = FastAPI()
chatbot = ChatBot()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join("pdf", file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    chatbot.load_pdf(file_path)
    return {"msg": "PDF 已加载"}

@app.post("/chat")
async def chat(query: str = Form(...)):
    response = chatbot.ask(query)
    return {"response": response}