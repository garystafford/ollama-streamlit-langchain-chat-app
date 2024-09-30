import argparse
from collections import defaultdict, Counter
import csv


def extract_names(csv_path: str) -> list[dict]:
    """
    Extracts 'First Name' values from a CSV file and returns them as a list of dictionaries.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains a unique name and its count.
    """

    # Initialize a Counter object to store unique names and their counts
    name_counts = Counter()

    with open(csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Check if the 'First Name' column exists in the current row
            if "First Name" in row:
                name = row["First Name"]
                name_counts[name] += 1

    # Convert the Counter object to a list of dictionaries and sort it
    result = [
        {"name": key, "count": value}
        for key, value in sorted(name_counts.items(), key=lambda x: (-x[1], x[0]))
    ]

    return result


def main() -> None:
    """
    The main function that parses command-line arguments and calls the extract_names function.
    """

    # Parse command-line argument
    parser = argparse.ArgumentParser(
        description="Extracts unique names from a CSV file."
    )
    parser.add_argument("csv_path", help="Path to the CSV file.")
    args = parser.parse_args()

    result = extract_names(args.csv_path)

    # Print the results in the desired format
    for name_dict in result:
        print(f'Name: {name_dict["name"]}, Count: {name_dict["count"]}')


if __name__ == "__main__":
    main()
