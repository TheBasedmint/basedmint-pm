import os
import requests
import yaml

def load_labels_yaml(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def get_github_token():
    # Ensure you have a GitHub token set as a secret in your repository
    return os.environ.get("GH_PAT")

def read_labels(repo, issue_number, labels):
    headers = {
        "Authorization": f"Bearer {get_github_token()}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels"
    response = requests.post(url, headers=headers, json=labels)

    if response.status_code == 200:
        print(f"Labels added successfully to issue #{issue_number} in repo {repo}")
    else:
        print(f"Failed to add labels to issue #{issue_number} in repo {repo}. Status code: {response.status_code}")
        print(response.text)

def main():
    # Path to the labels YAML file
    labels_file = '.github/scripts/labels.yml'

    # Load labels from YAML file
    labels_data = load_labels_yaml(labels_file)

    # GitHub organization name
    organization = 'your-organization'

    # Iterate through repositories in the organization
    for repo in ["repo1", "repo2", "repo3"]:  # Add your repositories here
        # Fetch all issues in the repository
        issues_url = f"https://api.github.com/repos/{organization}/{repo}/issues"
        issues_response = requests.get(issues_url, headers={"Authorization": f"Bearer {get_github_token()}"})
        
        if issues_response.status_code == 200:
            issues = issues_response.json()

            # Iterate through issues and re-add labels
            for issue in issues:
                try:
                    issue_number = issue['number']
                    print(f"Issue #{issue_number} in repo {repo}")
                    
                    # Extract removed labels from the issue if available
                    removed_labels = [label['name'] for label in issue.get('labels', []) if label['name'].lower() in (label_data['name'].lower() for label_data in labels_data)]

                    if removed_labels:
                        print(f"Re-adding labels: {removed_labels}")
                        read_labels(repo, issue_number, {"labels": removed_labels})
                    else:
                        print("No labels to re-add")
                except Exception as e:
                    print(f"Error processing issue: {e}")
        else:
            print(f"Failed to fetch issues in repo {repo}. Status code: {issues_response.status_code}")
            print(issues_response.text)

if __name__ == "__main__":
    main()
