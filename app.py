import sys
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

def main():
    st.markdown('<h1 class="header">Ask your CSV</h1>', unsafe_allow_html=True)

    # Add the link to the external CSS file
    st.markdown(
        """
        <link href="styles.css" rel="stylesheet">
        """,
        unsafe_allow_html=True
    )

    password_secret = st.secrets.get("PASSWORD")
    openai_secret = st.secrets.get("openai")

    if password_secret is None or openai_secret is None:
        st.error("Required secrets are missing. Please check your secrets configuration.")
        st.stop()

    password = st.text_input("Enter password:", type="password")
    if password != password_secret.get("password"):
        st.error("Invalid password. Access denied.")
        st.stop()

    user_csv = st.file_uploader("Upload your CSV file", type="csv")
    if user_csv is not None:
        user_question = st.text_input("Ask a question about your CSV:")
        agent = create_agent(user_csv)
        if agent is None:
            st.error("Failed to create the agent.")
            st.stop()

        if user_question is not None and user_question != "":
            st.write(f"Your question was: {user_question}")
            try:
                response = run_agent(agent, user_question)
                st.write(response)
            except Exception as e:
                st.error("An error occurred during agent execution.")
                st.error(str(e))

    st.write("Python version:", sys.version)

def create_agent(user_csv):
    openai_secret = st.secrets.get("openai")
    if openai_secret is None:
        return None

    openai_api_key = openai_secret.get("key")
    return create_csv_agent(
        OpenAI(openai_api_key=openai_api_key, temperature=0, model_name='gpt-3.5-turbo'),
        path=user_csv, verbose=True
    )

def run_agent(agent, user_question):
    return agent.run(user_question)

if __name__ == '__main__':
    main()
