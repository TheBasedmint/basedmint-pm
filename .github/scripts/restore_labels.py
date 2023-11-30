import os
import requests
import json

# Replace with your GitHub username, organization, repository, and personal access token
username = "JessieBroke"
organization = "TheBasedmint"
repository = "test1"
token = os.getenv("GH_PAT")

# GitHub API endpoint for listing issue events
api_url = f"https://api.github.com/repos/{organization}/{repository}/issues/events"

# Fetch issue events
response = requests.get(api_url, headers={"Authorization": f"Bearer {token}"})
events = response.json()

# Create the output directory if it doesn't exist
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Save events to a JSON file in the output directory
filename = os.path.join(output_dir, "issue_events.json")
with open(filename, "w") as file:
    json.dump(events, file)

# Restore labels based on deletion events
for event in events:
    if event["event"] == "label":
        label_name = event["label"]["name"]
        # Restore the label using your preferred method (GitHub API, gh CLI, etc.)
        print(f"Restoring label: {label_name}")
        # Add logic here to restore the label using the GitHub API or other methods
