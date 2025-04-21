# PDF文档问答助手

基于FastAPI和Streamlit构建的PDF文档问答系统，可以上传PDF文件并进行基于文档内容的问答。

## 功能特点

- 支持PDF文档上传和解析
- 基于向量数据库的文档内容检索
- 使用大语言模型进行问答
- 支持OpenAI和HuggingFace两种LLM提供商

## 环境准备

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 配置环境变量：

复制`.env`文件并填入自己的API密钥：
```
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai  # 可选值: openai 或 huggingface
```

如果使用HuggingFace模型，还需要设置：
```
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```

## 启动应用

方法一：使用运行脚本（推荐）
```bash
python run.py
```

方法二：分别启动后端和前端
```bash
# 终端1: 启动后端
uvicorn main:app --host 0.0.0.0 --port 8000

# 终端2: 启动前端
streamlit run app.py
```

## 使用方法

1. 打开浏览器访问 http://localhost:8501
2. 在左侧边栏上传PDF文档
3. 在主界面输入问题并点击发送
4. 查看AI助手的回答

## 技术架构

- FastAPI: 提供后端API服务
- Streamlit: 提供前端用户界面
- LangChain: 处理文档加载、分割和检索
- FAISS: 向量数据库，用于高效文本检索
- HuggingFace/OpenAI: 提供大语言模型能力 