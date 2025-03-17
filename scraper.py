import os
import json
import requests
from base64 import b64decode

# GitHub repository details
OWNER = "Blazemach-007"
REPO = "nlp-intro"
GITHUB_API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"

# (Optional) Add your GitHub token for higher API rate limits
GITHUB_TOKEN = ""  # Replace with your token or leave None for public repos
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

# Function to list all files in the repository
def get_files(path=""):
    url = f"{GITHUB_API_URL}/{path}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Function to fetch file content
def fetch_file_content(file_url):
    response = requests.get(file_url, headers=HEADERS)
    if response.status_code == 200:
        file_data = response.json()
        if "content" in file_data:
            try:
                # Attempt to decode as UTF-8 text
                return b64decode(file_data["content"]).decode("utf-8")
            except UnicodeDecodeError:
                # If decoding fails, return "binary file" message
                return None  
    return None

# Recursive function to get all files
def fetch_repo_data(path=""):
    repo_data = {}
    items = get_files(path)
    
    for item in items:
        if item["type"] == "file":  # Process files only
            content = fetch_file_content(item["url"])
            if content is not None:  # Only store valid text files
                repo_data[item["path"]] = content
        elif item["type"] == "dir":  # Recurse into directories
            repo_data.update(fetch_repo_data(item["path"]))

    return repo_data

# Fetch repository data
repo_data = fetch_repo_data()

# Save data to a JSON file (overwrite existing file)
output_file = "repo_data.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(repo_data, json_file, indent=4)

print(f"Repository data has been saved to {output_file}")
