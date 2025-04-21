
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
import jieba
from config.templates import QA_PROMPT


def extract_text_from_PDF(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    full_text = "\n".join([page.page_content for page in pages])
    return full_text

def split_content_into_chunks(text: str):
    seg_text = " ".join(jieba.cut(text))
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=100,
    )
    return splitter.create_documents([seg_text])

def save_chunks_into_vectorstore(content_chunks, embedding_model):
    return FAISS.from_documents(content_chunks, embedding_model)

def get_chat_chain(llm, vector_store, memory):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=False,
    )

def process_user_input(chain, query: str):
    return chain.run(query).strip()
