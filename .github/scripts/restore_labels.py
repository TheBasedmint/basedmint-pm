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

        # Upload the JSON file as an artifact using GitHub Actions command
        os.system(f'echo "::set-output name=artifacts::{filename}"')
        os.system(f'echo "::set-output name=artifact_paths::{filename}"')

    print("\n")
