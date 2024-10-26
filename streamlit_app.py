import streamlit as st
from urllib.parse import urlparse, parse_qs

st.title("Dynamic Page Input Example")

# Extract query parameters from the URL
query_params = st.experimental_get_query_params()

# Get the value from the query parameter
default_text = query_params.get("input", [""])[0]

# Input text box with the default value from the URL
user_input = st.text_input("Enter your text:", value=default_text)

# Display the user input
st.write(f"You entered: {user_input}")

# Update URL with the new input value
st.experimental_set_query_params(input=user_input)

# Show the current URL for reference
st.write(f"Current URL: {st.experimental_get_url()}")

