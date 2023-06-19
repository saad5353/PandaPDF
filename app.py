import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback


def get_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    return ''.join(page.extractText() for page in pdf_reader.pages)


def split_text(text):
    splitter = CharacterTextSplitter(chunk_size=500, separator='\n', chunk_overlap=100, length_function=len)
    return splitter.split_text(text)
    
    

def main():
    load_dotenv()
    st.set_page_config(page_title='PandaPDF', page_icon=':panda_face:')
    st.header('PandaPDF 🐼')
    st.subheader('Chat with your PDFs')
    st.write('This is a simple web app that lets you chat with your PDFs. Upload your PDF and start chatting with it. 🤖') 
    uploaded_file = st.file_uploader("Upload your File", type=['pdf']) 
    if uploaded_file is not None:
        file_text = get_text_from_pdf(uploaded_file)
        if file_text == '':
            st.error('🚩 PDF does not contain any text. Please upload another PDF.')
        else:
            split_texts = split_text(file_text)
            embeddings = OpenAIEmbeddings()
            knowledge_base = FAISS.from_texts(split_texts, embeddings)
            query = st.text_input('Ask your PDF a question 🤔')
            if query:
                with st.spinner('🔍 Searching for answer...'):
                    docs = knowledge_base.similarity_search(query)
                    llm = OpenAI()
                    chain = load_qa_chain(llm, chain_type='stuff')
                    with get_openai_callback() as callback:
                        response = chain.run(input_documents=docs, question=query)
                        print(callback) 
                st.success(f'🎉 {response}')


   



if __name__ == '__main__':
    main()