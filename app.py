
import streamlit as st
import subprocess

# Install langchain
subprocess.check_call(["pip", "install", "langchain"])

from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

def create_agent(user_csv):
    return create_csv_agent(
        OpenAI(openai_api_key=st.secrets["openai"]["key"],
               temperature=0, model_name='gpt-3.5-turbo'),
        path=user_csv, verbose=True
    )

def run_agent(agent, user_question):
    return agent.run(user_question)

# Apply CSS styling to the app
st.markdown(
    """
    <style>
    body {
        background-color: #F2F2F2;  /* Set a light gray background color */
        font-family: Arial, sans-serif;  /* Use a clean sans-serif font */
    }
    .header {
        font-size: 36px;
        color: #008080;  /* Set a refreshing teal color */
        padding: 16px;
        text-align: center;
    }
    .button {
        background-color: #008080;  /* Set a refreshing teal color */
        color: #FFFFFF;  /* Set white text color */
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.markdown('<h1 class="header">Ask your CSV</h1>', unsafe_allow_html=True)

    password = st.text_input("Enter password:", type="password")
    if password != st.secrets["PASSWORD"]["password"]:
        st.stop()

    user_csv = st.file_uploader("Upload your CSV file", type="csv")
    if user_csv is not None:
        user_question = st.text_input("Ask a question about your CSV:")
        agent = create_agent(user_csv)
        if user_question is not None and user_question != "":
            st.write(f"Your question was: {user_question}")
            response = run_agent(agent, user_question)
            st.write(response)

if __name__ == '__main__':
    main()
