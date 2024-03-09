import os 
import streamlit as st 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DeepLake
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import format_document
from langchain_core.runnables import RunnableParallel
from operator import itemgetter
from langchain_core.messages import get_buffer_string, AIMessage, HumanMessage


os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN')
os.environ['DEEPLAKE_ACCOUNT_NAME']= os.getenv('DEEPLAKE_ACCOUNT_NAME')

st.set_page_config(page_title="Chatbot", page_icon="💬", layout="centered")


@st.cache_resource
def connecting_to_the_database():
    embeddings = OpenAIEmbeddings()
    db = DeepLake(
    dataset_path=f"hub://AleVivi/digital_CV",
    read_only=True,
    embedding_function=embeddings,
    )
    retriever = db.as_retriever()
    
    return retriever

retriever = connecting_to_the_database()



_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are a chatbot with the task of convincing users to hire Alessandro Viviani at their company. 
The absence of information regarding something doesn't imply its negation, if you don't know something just say it. Give brief but impactful answers to their question considering the following context:
{context}

Question: {question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(template)


DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")


def _combine_documents(docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


_inputs = RunnableParallel(
    standalone_question=RunnablePassthrough.assign(
        chat_history=lambda x: get_buffer_string(x["chat_history"])
    )
    | CONDENSE_QUESTION_PROMPT
    | ChatOpenAI(temperature=0.8)
    | StrOutputParser()
)
_context = {
    "context": itemgetter("standalone_question") | retriever | _combine_documents,
    "question": lambda x: x["standalone_question"],
}
conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | ChatOpenAI(temperature=0.8)


def reset_conversation():
    del st.session_state.messages



def main():
    st.title("Chatbot 🤖💬")

    #col1, col2 = st.columns(2, gap="large")
    tab1, tab2 = st.tabs(["Description", "Brief explanation of the model"])
    with tab1:
        st.subheader("Description:")
        st.write(
        """
        This chatbot will try to convince you to hire me to your company! 😃 \n
        He knows much more informations about me than what you would find in my CV, so try to ask him some questions. If you want to restart the conversation press the button below.
        """)
        st.button('Reset Chat', on_click=reset_conversation)

    with tab2:
        st.subheader("Brief explanation of the model:")
        st.write(
        """
        This chatbot was made using the LangChain framework, which allows you to combine the power of 
        Chatgpt and the knowledge stored inside a database. This enable the chatbot to be context-aware: the language 
        model has access to informations, prompt instructions and examples that helps him solve its specific task in
        its specific setting. \n
        To go more in detail, I used a vector database called Deep Lake. Chatgpt retrieves only the informations that have 
        similarities with the user's question. He also takes into consideration the chat history and the prompt of 
        convincing the user to hire me. With all these elements it formulates an answer.
        """
        )
        st.write("---")


    client = conversational_qa_chain

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Why should I hire Alessandro?"):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            messages = []
            for m in st.session_state.messages:
                if m["role"] == "assistant":
                    lang_message = AIMessage(content = str(m["content"]))
                    messages.append(lang_message)
                    print(lang_message)
                if m["role"] == "user":
                    lang_message = HumanMessage(content = str(m["content"]))
                    messages.append(lang_message)
                    print(lang_message)

            response = client.invoke(
                {
                "question": prompt,
                "chat_history": messages,
                }
            )
            st.write(response.content)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response.content})


if __name__ == "__main__":
    main()


