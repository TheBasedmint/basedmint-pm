import os
import requests
import json

# Replace with your GitHub username, organization, and personal access token
username = "JessieBroke"
organization = "TheBasedmint"
repositories = ["test1", "test2"]  # Add additional repositories here
token = os.getenv("GH_PAT")

def fetch_issue_events(repository):
    api_url = f"https://api.github.com/repos/{organization}/{repository}/issues/events"
    response = requests.get(api_url, headers={"Authorization": f"Bearer {token}"})
    return response.json() if response.status_code == 200 else None

def save_issue_events(repository, events):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{repository}_issue_events.json")
    with open(filename, "w") as file:
        json.dump(events, file)

def restore_labels(events):
    for event in events:
        if event["event"] == "label":
            label_name = event["label"]["name"]
            # Restore the label using your preferred method (GitHub API, gh CLI, etc.)
            print(f"Restoring label: {label_name}")
            # Add logic here to restore the label using the GitHub API or other methods

if __name__ == "__main__":
    for repository in repositories:
        print(f"Fetching issue events for {repository}")
        events = fetch_issue_events(repository)

        if events:
            save_issue_events(repository, events)
            restore_labels(events)
