import json

# Constants
NAME = "Name"
RATIO = "Ratio"
WEIGHT = "Weight"
EXCLUDED_KEYS = [NAME, RATIO, WEIGHT]


def load_armor_data():
    """
    Load armor data from a JSON file.
    """
    with open("armors.json", "r") as file:
        return json.load(file)


def get_armor_attributes(armor_data):
    """
    Get the attributes of the armor from the armor data.
    """
    return [
        key
        for key in armor_data[next(iter(armor_data.keys()))][0].keys()
        if key not in EXCLUDED_KEYS
    ]


def get_user_selected_attribute(armor_attributes):
    """
    Get the attribute selected by the user from the list of armor attributes.
    """
    print("Select a parameter to maximize:")
    for i, attribute in enumerate(armor_attributes, start=1):
        print(f"{i}. {attribute}")
    selected_index = int(input("Enter the number of the parameter: ")) - 1
    return armor_attributes[selected_index]
