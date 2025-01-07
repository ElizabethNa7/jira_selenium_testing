import json

def load_test_data(test_data):
    with open(test_data, 'r') as file:
        return json.load(file)

# Usage example
test_data = load_test_data('utils/test_data.json')
print(test_data['login']['valid_user']['username'])  # Output: valid_user
