import json

def read_json(file_path: str) -> dict:
    """Reads a JSON file with error handling."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise IOError(f"Failed to read {file_path}: {str(e)}")

def write_json(file_path: str, data: dict) -> None:
    """Writes data to a JSON file with error handling."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        raise IOError(f"Failed to write {file_path}: {str(e)}")
