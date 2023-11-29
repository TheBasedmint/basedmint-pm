import os
import requests
import json

def fetch_issue_events(username, organization, repository, token):
    # GitHub API endpoint for listing issue events
    api_url = f"https://api.github.com/repos/{organization}/{repository}/issues/events"

    # Fetch issue events
    response = requests.get(api_url, headers={"Authorization": f"Bearer {token}"})
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch issue events for {repository}. Status code: {response.status_code}")
        return None

def fetch_all_repositories(username, organization, token):
    # GitHub API endpoint for listing repositories in the organization
    api_url = f"https://api.github.com/orgs/{organization}/repos"

    # Fetch repositories
    response = requests.get(api_url, headers={"Authorization": f"Bearer {token}"})
    
    # Check if the request was successful
    if response.status_code == 200:
        return [repo["name"] for repo in response.json()]
    else:
        print(f"Failed to fetch repositories for {organization}. Status code: {response.status_code}")
        return []

# Replace with your GitHub username, organization, and personal access token
username = "JessieBroke"
organization = "codex-storage"
token = os.getenv("GH_PAT")

# Fetch all repositories in the organization
repositories = fetch_all_repositories(username, organization, token)

# Iterate over each repository and fetch issue events
for repository in repositories:
    print(f"Fetching issue events for {repository}")
    events = fetch_issue_events(username, organization, repository, token)

    if events:
        # Save events to a JSON file for each repository
        filename = f"{repository}_issue_events.json"
        with open(filename, "w") as file:
            json.dump(events, file)

        # Restore labels based on deletion events for each repository
        for event in events:
            if event["event"] == "label":
                label_name = event["label"]["name"]
                # Restore the label using your preferred method (GitHub API, gh CLI, etc.)
                print(f"Restoring label: {label_name} in {repository}")
                # Add logic here to restore the label using the GitHub API or other methods

        # Upload the JSON file as an artifact for each repository
        os.system(f'echo "::set-output name=artifacts::{filename}"')

    print("\n")
