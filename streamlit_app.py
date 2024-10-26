import streamlit as st
import os
import zipfile
import requests
import uuid
import json
from urllib.parse import urlparse, parse_qs
st.set_page_config(
    page_title="MCAddon Manager",
    page_icon="mcaddon-logo.ico"
    
)
#Functions:
#UUID Gen
def generate_uuids():
    return str(uuid.uuid4()), str(uuid.uuid4())
#Manifest Modifications
def modify_manifest(source_dir, delay, is_void_gen):
    manifest_path = os.path.join(source_dir, 'manifest.json')
    uuid1, uuid2 = generate_uuids()
    with open(manifest_path, 'r') as file:
        manifest_data = file.read()

    if manifest_option == '1':
        modified_manifest_data = manifest_data.replace(
            'packname', f'{packname1}'
        ).replace(
            'packdescription', f'{packdescription1}'
        )
    if manifest_option == '2':
       modified_manifest_data = manifest_data.replace(
            'packname', f'{packname2}'
        ).replace(
            'packdescription', f'{packdescription2}'
        )
    else:
        modified_manifest_data = manifest_data.replace(
            'packname', f'{packname2}'
        ).replace(
            'packdescription', f'{packdescription2}'
        )
        
    modified_manifest_data = modified_manifest_data.replace('uuid1', uuid1).replace('uuid2', uuid2).replace('timedelay', str(delay))
    
    with open(manifest_path, 'w') as file:
        file.write(modified_manifest_data)
def zip_files_to_mcaddon(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(source_dir))
                zipf.write(file_path, arcname)
                
def upload_to_fileio(file_path):
    with open(file_path, 'rb') as file:
        response = requests.post('https://file.io', files={'file': file})
    response_data = response.json()
    return response_data.get('link')
#---------------------------------------- UI Starts Here ----------------------------------------
st.title("Dynamic Page Input Example")
main_option = st.selectbox('Choose an option:', ['Open-Source', '-Changelogs-'])
if main_option == 'Open-Source':
    user_input = st.text_input("Enter your text:")
    st.write(f"Current URL: https://mcaddon-manager.streamlit.app/?url={user_input}")

    st.write(f"Current URL: https://mcaddon-manager.streamlit.app/?url={user_input}")

if main_option == '-Changelogs-':
    
    st.markdown("## **Addon Manager | 0.01:**")
    st.markdown("-\n - Date: *10/25/2024*")
    st.write("---")
