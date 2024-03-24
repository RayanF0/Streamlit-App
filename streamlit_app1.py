import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.title('AI Chat')

api_key= "AIzaSyDBqhTqP1aVHncdKeGER4lOUTYkc9sSdN4" 

genai.configure(api_key=api_key)

generation_config = { # paramaters for ai response
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [ # list of safety features 
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

def read_pdf(content): # extracts text from pdf
    text = "" # empty string to store text
    for page in PdfReader(content).pages: # iterates through pdf pages
        text = text + page.extract_text() # append text from current page to the empty string
    return text


if 'history' not in st.session_state: #initalizes history queue and makes sure that history can store data while the app is running
    st.session_state['history'] = []

def enqueue_history(query, response): # adds a message to the history  
    if len(st.session_state['history']) >= 10: # after the queue reaches 10 it will begin popping
        st.session_state['history'].pop(0)
    st.session_state['history'].append((query, response)) # else it will append the query and response

with st.form('chat_form'): # creates input field
    userinput = st.text_area('Enter message:', '') # creates text area
    pdffile = st.file_uploader("Upload PDF", type=["pdf"]) # creates area to upload pdf
    submit = st.form_submit_button('Submit')

    if 'chat' not in st.session_state: # checks if chat has been initalized
        st.session_state['chat'] = model.start_chat(history=st.session_state['history']) #creates chat session and passes history
    chat = st.session_state['chat']#assigns it to var chat
    if submit:
        if userinput: 
            chat.send_message(userinput) # sends chat as text to session
            enqueue_history("👤 User", userinput) #enque function
            AI = chat.last.text #checks latest message
            enqueue_history("🤖 AI", AI) # enque function
        if pdffile: # same logic as userinput
            pdftext = read_pdf(pdffile)
            chat.send_message(pdftext) 
            enqueue_history("👤 User"," ") 
            AI = chat.last.text 
            enqueue_history("🤖 AI", AI) 


st.subheader("History")
for query, response in st.session_state['history']: # loops through user query and ai response 
    st.write(query + ":") # displays the text 
    st.write(response)
    

   
