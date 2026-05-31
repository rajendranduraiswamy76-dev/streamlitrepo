import streamlit as st

st.title("Hello Streamlit-er 👋")


st.text("sub page 1")
st.markdown("_Markdown_")

st.page_link("pages/widgets_demo.py", label="Go to interactive widgets demo page")


if st.button("Send balloons!"):
    st.balloons()
