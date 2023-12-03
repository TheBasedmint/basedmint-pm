import json
from github import Github
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# GitHub token
github_token = os.getenv("GH_PAT")

# Create a GitHub instance
g = Github(github_token)

def reapply_labels(repo_name, json_file_path):
    # Load JSON data
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Get the repository
    repo = g.get_repo(repo_name)

    # Iterate through issues in the JSON file
    for issue_data in data:
        issue_number = issue_data["issue_number"]
        labels = issue_data["labels"]

        # Get the issue
        issue = repo.get_issue(number=issue_number)

        # Clear existing labels
        issue.set_labels()

        # Apply new labels
        for label in labels:
            issue.add_to_labels(label)

if __name__ == "__main__":
    # Replace with your repository name and JSON file path
    repository_name = "your/repository"
    json_file_path = "path/to/your/json/file.json"

    # Call the function to reapply labels
    reapply_labels(repository_name, json_file_path)
