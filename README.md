**MCQ2MCQ**

All credit goes to Langchain & Streamlit for this project.

Demo - https://mcqt2mcq.streamlit.app/

**Overview**

MCQ2MCQ is a Python application powered by GPT that allows users to upload documents and generate multiple-choice questions (MCQs) in a structured format. Built with LangChain and Streamlit, this application aims to facilitate the creation of quizzes, assessments, or study materials by automating the process of question generation.

![image](https://github.com/Heathen2/quiz-from-text/assets/34716154/c6972f64-7b03-46b3-926f-3c692437f3b1)
![image](https://github.com/Heathen2/quiz-from-text/assets/34716154/07283cf6-3d1c-4224-a50e-4b620553100e)
![image](https://github.com/Heathen2/quiz-from-text/assets/34716154/ce51bee1-c23f-43f3-affc-4e53ccbaf9bf)
![image](https://github.com/Heathen2/quiz-from-text/assets/34716154/03a70849-b627-4efc-adcb-61e76e043b5d)


**Features**

MCQ Document Upload: Users can upload text documents in various formats (e.g., PDF, DOCX, TXT) containing the MCQ content from which MCQs need to be generated.

Question Generation: The application utilizes LangChain, a natural language processing library, to analyze the uploaded documents and generate relevant multiple-choice questions.

MCQ Sheet Creation: Generated MCQs are presented in a standardized format suitable for printing or digital sharing, facilitating easy integration into educational materials or assessments.

Streamlit Interface: The user-friendly Streamlit interface ensures seamless interaction, allowing users to upload documents and obtain MCQ outputs effortlessly.


**Installation**

To run the LangChain MCQ Generator locally, follow these steps:

Clone the repository:

bash

    git clone https://github.com/athulaugustine/MCQ2MCQ-Automated-Multiple-Choice-Questions-Extractor.git

Navigate to the project directory:

bash

    cd quiz-from-text

Install the required dependencies:

    pip install -r requirements.txt

Run the application:

    streamlit run streamlit_app.py

**Usage**

Launch the application by running streamlit run streamlit_app.py.
Upload a document containing the content for which MCQs need to be generated.
Click on the "Extract" button to initiate the question generation process.
Once the MCQs are generated, they will be displayed on the interface.
Optionally, you can Download the generated MCQs as a formatted sheet for further use.
