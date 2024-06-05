from typing import Any, Dict, List


def flatten_json(nested_json: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested JSON object while keeping keys in camelCase and using a distinct separator for nested keys.
    
    Parameters:
        nested_json (Dict[str, Any]): The JSON object to flatten.
        separator (str): The separator used to denote nesting in the keys.
    
    Returns:
        Dict[str, Any]: A dictionary with flattened keys.
    """
    flattened_dict = {}

    def flatten(current_element: Any, key_prefix: str = '') -> None:
        """
        Recursively flattens the JSON object.
        
        Parameters:
            current_element (Any): Current element to be flattened.
            key_prefix (str): Accumulated key formed from nested dictionary keys.
        """
        if isinstance(current_element, dict):
            for key, value in current_element.items():
                flatten(value, key_prefix + key + separator)
        elif isinstance(current_element, list):
            for index, item in enumerate(current_element):
                flatten(item, key_prefix + str(index) + separator)
        else:
            flattened_dict[key_prefix.rstrip(separator)] = current_element

    flatten(nested_json)
    return flattened_dict


def flatten_list_of_dicts(list_of_dicts: List[Dict[str, Any]], separator: str = '.') -> List[Dict[str, Any]]:
    """
    Flattens a list of nested JSON-like dictionaries, applying the flatten_json function to each dictionary.

    Parameters:
        list_of_dicts (List[Dict[str, Any]]): A list of dictionaries to be flattened.
        separator (str): The separator used to denote nesting in the keys, passed to flatten_json.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries where each dictionary has been flattened.
    """
    flattened_dicts = []
    for nested_dict in list_of_dicts:
        flattened_dict = flatten_json(nested_dict, separator)
        flattened_dicts.append(flattened_dict)
    return flattened_dicts