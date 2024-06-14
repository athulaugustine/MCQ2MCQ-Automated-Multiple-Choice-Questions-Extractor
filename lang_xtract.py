from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import PyMuPDFLoader,Docx2txtLoader,TextLoader,PyPDFLoader,PyPDFium2Loader
import pandas as pd
from datetime import datetime
import os
import time

quiz_list = []
output_path = "output/Final_Quiz.xlsx"
temp_directory="temp/"
if not os.path.exists('temp'):
            os.makedirs('temp')
if not os.path.exists('output'):
            os.makedirs('output')            

def clear_all():
    quiz_list.clear()
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
            pass
        except OSError as e:
            pass

    if os.path.exists(temp_directory):
        try:
            files = os.listdir(temp_directory)
            for file in files:
                file_path = os.path.join(temp_directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except OSError as e:
            pass

    
        

class Question(BaseModel):
    """A question along with multiple-choice options and the correct answer."""
    question: str = Field(default=None, description="The quiz question.")
    option_a: str = Field(default=None, description="Option 'a' for the question.")
    option_b: str = Field(default=None, description="Option 'b' for the question.")
    option_c: str = Field(default=None, description="Option 'c' for the question.")
    option_d: str = Field(default=None, description="Option 'd' for the question.")
    correct_option: str = Field(default=None, description="The correct option, which is one of 'a', 'b', 'c', or 'd'.")
    answer: str = Field(default=None, description="The answer to the question.")


class Data(BaseModel):
    """List of questions."""
    Questions: List[Question]


def extract_quiz(api_key, file_content):
    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "As an expert educator, you're entrusted with the crucial task of crafting meticulously structured multiple-choice questions (MCQs) for an upcoming examination. "
                    "Commence by conducting a comprehensive analysis of the provided textbook passage, ensuring a profound comprehension to unearth all potential question avenues. "
                    "Subsequently, meticulously formulate each question, ensuring utmost clarity, with four plausible options, clearly indicating the correct option 'a','b','c' or 'd', and the answer for the question. "
                    "It's imperative that each question accurately reflects any mathematical expressions, if present, within the text. "
                    "Your role entails the scrupulous examination and rectification of any discrepancies in questions, options, correct option, and answer."
                ),
                ("human", "{text}"),
            ]
        )

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key
        )
        questions = []
        runnable = prompt | llm.with_structured_output(schema=Data)

        for page in file_content:
            try:
                time.sleep(61)
                response = runnable.invoke({"text": page.page_content})
                questions.extend(response.Questions)
                quiz_list.extend(response.Questions)
            except Exception as e:
                # Handle rate limit exceptions or any other API-related errors here
                print("Error:", e)
                # Optionally, you can re-raise the exception if needed
                raise

        # Convert questions to dictionary for easier handling
        data = {
            "question": [q.question for q in questions],
            "option_a": [q.option_a for q in questions],
            "option_b": [q.option_b for q in questions],
            "option_c": [q.option_c for q in questions],
            "option_d": [q.option_d for q in questions],
            "correct_option": [q.correct_option for q in questions],
            "answer": [q.answer for q in questions]
        }

        # Convert dictionary to DataFrame
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"temp/Questions_{timestamp}.xlsx"
        # Write DataFrame to Excel file
        df.to_excel(file_name, index=False)

    except Exception as e:
        # Handle any other exceptions that might occur
        print("Error:", e)
        # Optionally, you can re-raise the exception if needed
        raise





def get_quiz(api_key, doc_name,file_type):
    clear_all()
    text_splitter =  CharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=20,
        # length_function=len,
        # is_separator_regex=False,
    )
    
    try:
        if file_type == 'pdf':
            try:
                loader = PyMuPDFLoader(doc_name)
                file_content = loader.load_and_split(text_splitter=text_splitter)
                print(file_content[0].page_content)
            except:
                loader = PyPDFLoader(doc_name)
                file_content = loader.load_and_split(text_splitter=text_splitter)
            else:
                 pass        
        elif file_type == 'docx' or file_type=='doc':
            loader = Docx2txtLoader(doc_name)
            file_content = loader.load_and_split(text_splitter=text_splitter)
        elif file_type == 'txt':
            loader = TextLoader(doc_name,encoding='utf-8')
            file_content = loader.load_and_split(text_splitter=text_splitter)
    except:
         pass
    
    file_content_length = len(file_content)
    for i in range(0, file_content_length, 20):
        if i + 20 > file_content_length:
            try:
                extract_quiz(api_key,file_content[i:file_content_length])
            except:
                 pass    
        else:
            try:
                extract_quiz(api_key,file_content[i:i+20])
            except:
                 pass       

    data = {
            "question": [q.question for q in quiz_list],
            "option_a": [q.option_a for q in quiz_list],
            "option_b": [q.option_b for q in quiz_list],
            "option_c": [q.option_c for q in quiz_list],
            "option_d": [q.option_d for q in quiz_list],
            "correct_option": [q.correct_option for q in quiz_list],
            "answer": [q.answer for q in quiz_list]
        }

    # Convert dictionary to DataFrame
    df = pd.DataFrame(data)
    # Write DataFrame to Excel file
    df.to_excel(output_path, index=False)
    return df