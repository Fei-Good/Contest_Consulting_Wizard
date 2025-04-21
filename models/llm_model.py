from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFaceHub
# models/llm_model.py

import os
from dotenv import load_dotenv

# 确保环境变量已加载
load_dotenv()

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "openai")  # 支持 openai / huggingface
    
    if provider == "huggingface":
        huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if not huggingface_token:
            raise ValueError("使用HuggingFace需要设置HUGGINGFACEHUB_API_TOKEN环境变量")
        return HuggingFaceHub(
            repo_id="deepseek-ai/deepseek-llm-7b-chat",
            model_kwargs={"temperature": 0.7, "max_new_tokens": 512},
            huggingfacehub_api_token=huggingface_token
        )
    else:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("使用OpenAI需要设置OPENAI_API_KEY环境变量")
        return ChatOpenAI(temperature=0.7, api_key=openai_api_key)
