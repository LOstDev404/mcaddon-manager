import streamlit as st
from urllib.parse import urlparse, parse_qs
main_option = st.selectbox('Choose an option:', ['Open-Source', '-Changelogs-'])
st.title("Dynamic Page Input Example")
if main_option == 'Open-Source':
  query_params = st.experimental_get_query_params()
  default_text = query_params.get("input", [""])[0]
  user_input = st.text_input("Enter your text:", value=default_text)
  st.write(f"You entered: {user_input}")
  st.experimental_set_query_params(input=user_input)
  st.write(f"Current URL: `https://mcaddon-manager.streamlit.app/?input={user_input}'")

if main_option == '-Changelogs-':
    
    st.markdown("## **`Addon Manager | 0.01`:**")
    st.markdown("-\n - Date: *10/25/2024*")
    st.write("---")

