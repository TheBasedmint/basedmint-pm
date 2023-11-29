import os
import requests

# Replace with your GitHub username, organization, repository, and personal access token
username = "JessieBroke"
organization = "TheBasedmint"
repository = "basedmint-pm"
token = os.getenv("GH_PAT")

# GitHub API endpoint for listing label events
api_url = f"https://api.github.com/repos/{organization}/{repository}/issues/events"

# Fetch label deletion events
response = requests.get(api_url, headers={"Authorization": f"Bearer {token}"})
events = response.json()

# Restore labels based on deletion events
for event in events:
    if event["event"] == "label":
        label_name = event["label"]["name"]
        # Restore the label using your preferred method (GitHub API, gh CLI, etc.)
        print(f"Restoring label: {label_name}")
        # Add logic here to restore the label using the GitHub API or other methods