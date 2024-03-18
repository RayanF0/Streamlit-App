# AIzaSyDBqhTqP1aVHncdKeGER4lOUTYkc9sSdN4

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import fitz

st.title('AI Chat')

api_key= "AIzaSyDBqhTqP1aVHncdKeGER4lOUTYkc9sSdN4"

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def read_pdf(content):
    pdfdoc= fitz.open(stream=content,filetype="pdf")
    text=""
    for page in pdfdoc:
        text= text+ page.get_text()
    return text

if 'history' not in st.session_state:
    st.session_state['history']= []

def push_history(speaker, message):
    if len(st.session_state['history'])>= 10:
        st.session_state['history'].pop(0)
    st.session_state['history'].append((speaker, message))

with st.form('chat_form'):
    userinput= st.text_area('Enter message:', '')
    pdffile= st.file_uploader("Upload PDF", type=["pdf"])
    submit= st.form_submit_button('Submit')

    if 'chat' not in st.session_state:
        st.session_state['chat'] = model.start_chat(history=st.session_state['history'])
    chat = st.session_state['chat']

    if submit:
        if pdffile:
            pdf_text = read_pdf(pdffile.getvalue())
            chat.send_message(pdf_text)
            push_history("User","Uploaded PDF")
            AI= chat.last.text
            push_history("AI",AI)
        if userinput:
            chat.send_message(userinput)
            push_history("User",userinput)
            AI= chat.last.text
            push_history("AI",AI)

st.subheader("History")
for speaker, message in st.session_state['history']:
    st.write(speaker + ":", message)
if __name__ == "__main__":
    main()
