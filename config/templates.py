from langchain.prompts import PromptTemplate

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
你是一个专业的文档问答助手，请结合以下文档内容回答用户问题。

文档内容：
{context}

用户提问：
{question}

请用简洁准确的语言回答。
"""
)