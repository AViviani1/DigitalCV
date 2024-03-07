import streamlit as st 

st.set_page_config(page_title="Thanks", page_icon="😄", layout="centered")

st.title("Thanks 😄")
st.markdown("""##### Thank you for taking your time to have a look at my website! #####""")
st.markdown("""##### Did you enjoy it? #####""")


if "feedback" not in st.session_state:
    st.session_state.feedback = "Don't know 😐"

def surprise():
    if st.session_state['feedback'] == "Yes! 🥳🎈":
        st.balloons()


feedback = st.radio(
    label = "**Did you enjoied it?**",
    options = ["Don't know 😐", "No 🙁", "Yes! 🥳🎈"],
    index = 0,
    horizontal = True,
    label_visibility = "collapsed",
    key = "feedback",
    on_change = surprise()
)
