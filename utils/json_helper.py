# module to help load data from JSON files to be used in tests
import json
import os

def load_test_data(test_data):
    if not os.path.exists(test_data):
        raise FileNotFoundError(f"{test_data} not found")
    try:
        with open(test_data, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {test_data}: {e}")
    # print(test_data['login']['valid_user']['username'])  # Output: valid_user

    # Get the absolute path of the current script (json_helper.py)
    # base_path = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(base_path, test_data)

    # try:
    #     with open(test_data, 'r') as file:
    #         return json.load(file)
    # except FileNotFoundError:
    #     raise FileNotFoundError(f"JSON file not found: {test_data}")
    # except json.JSONDecodeError:
    #     raise ValueError(f"Invalid JSON format in file: {test_data}")


# # Usage example
# test_data = load_test_data('utils/test_data.json')
# print(test_data['login']['valid_user']['username'])  # Output: valid_user
