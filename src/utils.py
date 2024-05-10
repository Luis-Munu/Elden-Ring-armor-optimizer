import json
from typing import Dict, List

# Constants
NAME = "Name"
RATIO = "Ratio"
WEIGHT = "Weight"
EXCLUDED_KEYS = [NAME, RATIO, WEIGHT]


def load_armor_data() -> Dict:
    """
    Load armor data from a JSON file.

    Returns
    -------
    Dict
        The armor data loaded from the JSON file.
    """
    with open("data/armors.json", "r") as file:
        return json.load(file)


def get_armor_attributes(armor_data: Dict) -> List[str]:
    """
    Get the attributes of the armor from the armor data.

    Parameters
    ----------
        armor_data : Dict
            The armor data.

    Returns
    -------
    List[str]
        The list of armor attributes.
    """
    return [
        key
        for key in armor_data[next(iter(armor_data.keys()))][0].keys()
        if key not in EXCLUDED_KEYS
    ]


def get_user_selected_attribute(armor_attributes: List[str]) -> str:
    """
    Get the attribute selected by the user from the list of armor attributes.

    Parameters
    ----------
        armor_attributes : List[str]
            The list of armor attributes.

    Returns
    -------
    str
        The attribute selected by the user.
    """
    print("Select a parameter to maximize:")
    for i in range(0, len(armor_attributes), 4):
        attributes_to_print = armor_attributes[i : i + 4]
        for j, attribute in enumerate(attributes_to_print, start=i + 1):
            print(f"{j}. {attribute}", end=" ")
        print()
    selected_index = int(input("Enter the number of the parameter: ")) - 1
    return armor_attributes[selected_index]
