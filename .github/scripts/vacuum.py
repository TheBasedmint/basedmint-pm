import os
import requests
import json
from datetime import datetime, timedelta

# Function to fetch issue events from GitHub API
def fetch_issue_events(repository):
    api_url = f"https://api.github.com/repos/{organization}/{repository}/issues/events"
    response = requests.get(api_url, headers={"Authorization": f"Bearer {token}"})
    return response.json() if response.status_code == 200 else None

# Function to save issue events to a JSON file
def save_issue_events(repository, events):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"{repository}_issue_events.json")
    with open(filename, "w") as file:
        json.dump(events, file)

# Function to restore labels based on deletion events
def restore_labels(events):
    for event in events:
        if event["event"] == "label":
            label_name = event["label"]["name"]
            # Restore the label using your preferred method (GitHub API, gh CLI, etc.)
            print(f"Restoring label: {label_name}")
            # Add logic here to restore the label using the GitHub API or other methods

# Function to filter issue events and extract unique issues
def filter_and_extract(events):
    # Calculate the datetime 48 hours ago from now
    time_threshold = datetime.utcnow() - timedelta(hours=48)

    # Create a dictionary to store unique issues based on issue URL
    unique_issues = {}

    # Iterate through each event in the list
    for event in events:
        # Extracting information for each event
        event_type = event.get('event')
        created_at_str = event.get('created_at')

        # Convert created_at string to datetime object
        created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")

        # Check if the event is 'unlabeled' and updated in the past 48 hours
        if event_type == 'unlabeled' and created_at > time_threshold:
            actor_login = event.get('actor', {}).get('login')
            label_name = event.get('label', {}).get('name')
            label_color = event.get('label', {}).get('color')
            issue_url = event.get('issue', {}).get('html_url')

            if actor_login and label_name and label_color and issue_url:
                # Check if the issue URL is not already in the dictionary
                if issue_url not in unique_issues:
                    unique_issues[issue_url] = {
                        'login': actor_login,
                        'label_name': label_name,
                        'label_color': label_color,
                        'issue_url': issue_url
                    }

    # Convert the dictionary values to a list
    filtered_data = list(unique_issues.values())

    # Write the filtered data to a new JSON file
    with open('output/vacuum_data.json', 'w') as output_file:
        json.dump(filtered_data, output_file, indent=2)

if __name__ == "__main__":
    # Replace with your GitHub username, organization, and personal access token
    username = "JessieBroke"
    organization = "TheBasedmint"
    repositories = ["test1", "test2"]  # Add additional repositories here
    token = os.getenv("GH_PAT")

    for repository in repositories:
        print(f"Fetching and processing issue events for {repository}")

        # Fetch issue events
        events = fetch_issue_events(repository)

        if events:
            # Save issue events to a file
            save_issue_events(repository, events)

            # Restore labels based on deletion events
            restore_labels(events)

    # Combine issue events from all repositories
    combined_events = []
    for repository in repositories:
        with open(f'output/{repository}_issue_events.json', 'r') as file:
            combined_events.extend(json.load(file))

    # Filter and extract unique issues
    filter_and_extract(combined_events)
