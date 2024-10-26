import os
import zipfile
import requests
import streamlit as st
import uuid
import json
import shutil
from urllib.parse import urlparse, parse_qs


st.set_page_config(
    page_title="MCAddon Manager",
    page_icon="mcaddon-logo.ico"
    
)
#---------------------------------------- UI Starts Here ----------------------------------------

st.title('MCADDON Custom Value Manager (Open Source `Version: 0.01`')
st.write('Contact `LOstDev404` on Discord for any bugs, questions, or suggestions.')

main_option = st.selectbox('Choose a pack / option:', ['Open-Source', '-Changelogs-'])

if main_option == 'Open-Source':
    query_params = st.experimental_get_query_params()

    default_text = query_params.get("input", [""])[0]
    user_input = st.text_input("Enter your text:", value=default_text)

    st.write(f"You entered: {user_input}")

    st.write(f"Current URL: {st.experimental_get_url()}")

if main_option == '-Changelogs-':

    st.write("---")
