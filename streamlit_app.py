import streamlit as st
import os
import requests
import uuid
import zipfile
from urllib.parse import urlparse

st.set_page_config(
    page_title="MCAddon Manager",
    page_icon="mcaddon-logo.ico"
)

# Functions:
# UUID Gen
def generate_uuids():
    return str(uuid.uuid4()), str(uuid.uuid4())

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

def zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

# Variable to track if the process has already run
process_completed = False

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
    if 'github.com' in parsed_url.netloc and not process_completed:
        path_parts = parsed_url.path.split('/')
        if len(path_parts) >= 5 and path_parts[3] == 'tree':
            repo_owner = path_parts[1]
            repo_name = path_parts[2]
            branch = path_parts[4]
            folder_path = '/'.join(path_parts[5:])

            output_dir = os.path.join("temp_download", folder_path)
            st.write(f"Downloading folder: {folder_path} from repo: {repo_owner}/{repo_name} (branch: {branch})")
            
            download_github_folder(repo_owner, repo_name, branch, folder_path, output_dir)
            
            # Zip the downloaded folder
            zip_name = f"{folder_path.replace('/', '_')}.zip"
            zip_folder(output_dir, zip_name)

            # Upload the zip file
            st.write(f"Uploading {zip_name} to file.io...")
            link = upload_to_fileio(zip_name)
            if link:
                st.success("Folder uploaded successfully.")
                st.write("Download link:")
                st.write(link)
            else:
                st.error("Failed to upload the zip file.")

            process_completed = True
        else:
            st.error("Invalid GitHub URL format. Please use a link to a folder in a repository.")

if main_option == '-Changelogs-':
    st.markdown("## **`Addon Manager | 0.01`:**")
    st.markdown("-\n - Date: *10/25/2024*")
    st.write("---")


