import streamlit as st
from lang_xtract import get_quiz


gpt_key = st.text_input("openai key",type="password")
if gpt_key:
    file_to_process = st.file_uploader("Upload the file",type=["pdf","docx","txt"])
    if file_to_process:
        file_type = file_to_process.name.split('.')[-1]
        process_btn = st.button("Extract")
        if process_btn:
            with st.spinner("Extracting"):
                if file_type=='pdf':
                    file_is = "input_to_process.pdf"
                    with open(file_is,'wb') as file:
                        file.write(file_to_process.getvalue())
                elif file_type=='docx' or file_type=='doc':
                    file_is = "input_to_process.docx"
                    with open(file_is,'wb') as file:
                        file.write(file_to_process.getvalue())
                elif file_type=='txt':
                    file_is = "input_to_process.txt"
                    with open(file_is,'wb') as file:
                        file.write(file_to_process.getvalue())                
                response = get_quiz(gpt_key, file_is,file_type)
                st.session_state["response"] = response
            st.success("Extracted and saved")
            with open("output/Final_Quiz.xlsx", "rb") as file:
                btn = st.download_button(
                label="Download",
                data=file,
                file_name="Final_Quiz.xlsx",
                )
            st.write(st.session_state["response"])
