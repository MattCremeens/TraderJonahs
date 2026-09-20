import json


def find_key_path(data, target_key, current_path=[]):
    # If it's a dictionary, search the keys
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = current_path + [f"'{key}'"]
            if key == target_key:
                return f"root[{']['.join(new_path)}]"
            
            # Recurse deeper
            result = find_key_path(value, target_key, new_path)
            if result: 
                return result

    # If it's a list, iterate through indices
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = current_path + [str(index)]
            result = find_key_path(item, target_key, new_path)
            if result: 
                return result
                
    return None



if __name__ == "__main__":
    f = open('run.txt', 'r')
    data = json.load(f)
    print(find_key_path(data, "arguments"))