import json
import os
import argparse

def correct_actions(data):
    """
    Recursively transforms lists with only numeric values to lists of size 1.

    Args:
        data: The JSON data (dict, list, or primitive).

    Returns:
        The transformed JSON data.
    """
    for action in data["Actions"]:
        print(action["actionName"])

        if "atWell" in action and isinstance(action["atWell"], dict):
            print("  Found 'atWell' dictionary, transforming...")
            well_data = action["atWell"]

            product_id_data = well_data.pop("productIdentification", None)

            if product_id_data is not None:
                action["productIdentification"] = product_id_data
                print(f"    Moved 'productIdentification': {product_id_data}")
            else:
                print("    'productIdentification' key not found within 'atWell'.")

        action["hasWell"] = well_data
        print(f"    Added 'hasWell' with remaining data: {well_data}")
        del action["atWell"]
        print("    Removed original 'atWell' key.")

    else:
        # Action does not have "atWell" key
        print("  No 'atWell' key found. Skipping transformation.")

    return data

def process_json_file(input_file, output_file):
    """
    Reads a JSON file, transforms it, and writes the transformed JSON to output.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file.
    """
    try:
        with open(input_file, 'r') as infile:
            json_data = json.load(infile)

        transformed_data = correct_actions(json_data)

        with open(output_file, 'w') as outfile:
            json.dump(transformed_data, outfile, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")

def main():
    """Parses command-line arguments and processes the JSON file."""
    parser = argparse.ArgumentParser(description="Transforms numeric lists in JSON.")
    parser.add_argument("input_file", help="Path to the input JSON file.")

    args = parser.parse_args()
    input_file = args.input_file

    # Derive output file name
    base_name, extension = os.path.splitext(input_file)
    output_file = f"{base_name}-corrected{extension}"

    process_json_file(args.input_file, output_file)

if __name__ == "__main__":
    main()
