# Write your functions for uploading the projects from csv file.. 
import pandas as pd
import os
import sys

def load_csv(file_path):
    """Load a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print("CSV file loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Error: There was an issue parsing the file.")
        sys.exit(1)

def save_data(df, output_file='validated_projects.csv'):
    """Save the DataFrame to a destination (e.g., CSV file)."""
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}.")

def main():
    # Specify the CSV file path here
    file_path = 'Hello-FOSS-SOC-Portal\socbackend\projects.csv'  # Change this to your CSV file path
    
    df = load_csv(file_path)

    save_data(df)

if __name__ == "__main__":
    main()



# Use projects.csv 
