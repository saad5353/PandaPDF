import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfFileReader

def main():
    load_dotenv()
    st.set_page_config(page_title='PandaPDF', page_icon=':panda_face:')
    st.header('PandaPDF 🐼')
    st.subheader('Your PDF to Chat Converter')
    st.write('👉 This is a simple web app that converts your PDF to a chat format.') 
    uploaded_file = st.file_uploader("Upload your File 📁", type=['pdf'])
   



if __name__ == '__main__':
    main()