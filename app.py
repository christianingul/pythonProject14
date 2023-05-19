import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI

def main():
    # Apply CSS styling to the app
    st.markdown(open("styles.css").read(), unsafe_allow_html=True)

    st.markdown('<h1 class="header">Ask your CSV</h1>', unsafe_allow_html=True)

    password = st.text_input("Enter password:", type="password")
    if password != st.secrets["PASSWORD"]["password"]:
        st.error("Invalid password. Access denied.")
        return

    user_csv = st.file_uploader("Upload your CSV file", type="csv")
    if user_csv is not None:
        user_question = st.text_input("Ask a question about your CSV:")
        agent = create_agent(user_csv)
        if user_question is not None and user_question != "":
            st.write(f"Your question was: {user_question}")
            response = run_agent(agent, user_question)
            st.write(response)

def create_agent(user_csv):
    return create_csv_agent(
        OpenAI(openai_api_key=st.secrets["openai"]["key"],
               temperature=0, model_name='gpt-3.5-turbo'),
        path=user_csv, verbose=True
    )

def run_agent(agent, user_question):
    return agent.run(user_question)

if __name__ == '__main__':
    main()
