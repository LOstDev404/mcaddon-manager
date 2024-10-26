import streamlit as st
import os
import zipfile
import requests
import uuid
import json
from urllib.parse import urlparse, parse_qs
from pathlib import Path

st.set_page_config(
    page_title="MCAddon Manager",
    page_icon="mcaddon-logo.ico"
)

# Functions:
# UUID Gen
def generate_uuids():
    return str(uuid.uuid4()), str(uuid.uuid4())

# Manifest Modifications
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

def download_github_folder(github_url, download_dir):
    api_url = github_url.replace('github.com', 'api.github.com/repos').replace('/tree/', '/contents/')
    response = requests.get(api_url)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            file_url = file['download_url']
            file_path = os.path.join(download_dir, file['name'])
            if file['type'] == 'file':
                with requests.get(file_url) as file_data:
                    with open(file_path, 'wb') as f:
                        f.write(file_data.content)
            elif file['type'] == 'dir':
                os.makedirs(file_path, exist_ok=True)
                download_github_folder(file['html_url'], file_path)
    else:
        st.error("Error downloading folder from GitHub")

#---------------------------------------- UI Starts Here ----------------------------------------
st.title("MCAddon Manager")
main_option = st.selectbox('Choose an option:', ['Open-Source', '-Changelogs-'])
if main_option == 'Open-Source':
    query_params = st.experimental_get_query_params()
    default_text = query_params.get("url", [""])[0]
    user_input = st.text_input("Enter GitHub URL:", value=default_text)
    st.experimental_set_query_params(url=user_input)
    
    if 'github.com' in user_input:
        folder_name = user_input.split('/')[-1]
        download_dir = os.path.join('downloads', folder_name)
        os.makedirs(download_dir, exist_ok=True)
        
        st.write(f"Downloading folder: `{folder_name}` from GitHub...")
        download_github_folder(user_input, download_dir)
        
        # Zip the folder
        zip_filename = f"{folder_name}.mcaddon"
        zip_files_to_mcaddon(download_dir, zip_filename)
        st.write(f"Zipped folder: `{zip_filename}`")
        
        # Upload to file.io
        st.write("Uploading to file.io...")
        fileio_link = upload_to_fileio(zip_filename)
        if fileio_link:
            st.success(f"Uploaded successfully! [Download here]({fileio_link})")
        else:
            st.error("Failed to upload to file.io")

if main_option == '-Changelogs-':
    st.markdown("## **`Addon Manager | 0.01`:**")
    st.markdown("-\n - Date: *10/25/2024*")
    st.write("---")
