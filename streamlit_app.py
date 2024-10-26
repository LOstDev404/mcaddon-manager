import streamlit as st
from urllib.parse import urlparse, parse_qs

st.title("Dynamic Page Input Example")
query_params = st.experimental_get_query_params()
default_text = query_params.get("input", [""])[0]
user_input = st.text_input("Enter your text:", value=default_text)
st.write(f"You entered: {user_input}")
st.experimental_set_query_params(input=user_input)
st.write(f"Current URL: `https://mcaddon-manager.streamlit.app/?input={user_input}")

