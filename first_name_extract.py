import pandas as pd


def extract_first_names(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Extract the 'First Name' column
    first_names = df["First Name"].tolist()

    # Remove duplicates and sort the values in ascending order
    unique_first_names = sorted(set(first_names))

    return unique_first_names


# Call the function with the CSV file name
first_names = extract_first_names("customers-100.csv")
print(first_names)
