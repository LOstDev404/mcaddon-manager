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

def download_github_folder(repo_owner, repo_name, branch, folder_path, output_dir):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}?ref={branch}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for item in contents:
            item_path = os.path.join(output_dir, item['name'])
            if item['type'] == 'file':
                download_file(item['download_url'], item_path)
            elif item['type'] == 'dir':
                download_github_folder(repo_owner, repo_name, branch, f"{folder_path}/{item['name']}", item_path)
    else:
        st.error("Error fetching the GitHub folder contents.")

def download_file(file_url, save_path):
    response = requests.get(file_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

# UI Starts Here
st.title("Dynamic Page Input Example")
main_option = st.selectbox('Choose an option:', ['Open-Source', '-Changelogs-'])

if main_option == 'Open-Source':
    query_params = st.experimental_get_query_params()
    default_text = query_params.get("url", [""])[0]
    user_input = st.text_input("Enter your URL:", value=default_text)
    st.experimental_set_query_params(url=user_input)
    
    # Parse the URL
    parsed_url = urlparse(user_input)
    if 'github.com' in parsed_url.netloc:
        path_parts = parsed_url.path.split('/')
        if len(path_parts) >= 5 and path_parts[2] == 'tree':
            repo_owner = path_parts[1]
            repo_name = path_parts[2]
            branch = path_parts[4]
            folder_path = '/'.join(path_parts[5:])
            
            output_dir = os.path.join("temp_download", folder_path)
            st.write(f"Downloading folder: {folder_path} from repo: {repo_owner}/{repo_name} (branch: {branch})")
            
            # Download the folder
            download_github_folder(repo_owner, repo_name, branch, folder_path, output_dir)
            
            # Zip and upload the folder to file.io
            zip_filename = f"{folder_path}.zip"
            zip_files_to_mcaddon(output_dir, zip_filename)
            
            fileio_link = upload_to_fileio(zip_filename)
            st.success(f"Folder uploaded to file.io: {fileio_link}")
        else:
            st.error("Invalid GitHub URL format. Please use a link to a folder in a repository.")

if main_option == '-Changelogs-':
    st.markdown("## **`Addon Manager | 0.01`:**")
    st.markdown("-\n - Date: *10/25/2024*")
    st.write("---")
