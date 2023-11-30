import yaml
import json

def load_labels_yaml(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def load_labels_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def write_labels_yaml(filename, data):
    with open(filename, 'w') as file:
        yaml.dump(data, file)

# Path to existing labels YAML file
existing_labels_file = '/home/broke/GitHub/basedmint-pm/.github/scripts/labels.yml'

# Path to new labels JSON file
new_labels_file = '/home/broke/GitHub/basedmint-pm/json/vacuum_data.json'

# Load existing labels
existing_labels_data = load_labels_yaml(existing_labels_file)

# Load new labels
new_labels_data = load_labels_json(new_labels_file)

# Get existing label names
existing_label_names = {label['name'].lower() for label in existing_labels_data}

# Populate new labels dynamically and avoid duplicates
new_labels = []
new_label_names = set()

for label in new_labels_data:
    label_name_lower = label["label_name"].lower()
    if label_name_lower not in existing_label_names and label_name_lower not in new_label_names:
        new_labels.append({
            "name": label["label_name"],
            "color": label["label_color"],
            "description": "",
        })
        new_label_names.add(label_name_lower)

# Add new labels to existing labels
existing_labels_data.extend(new_labels)

# Write updated labels to the YAML file
write_labels_yaml(existing_labels_file, existing_labels_data)
