import pandas as pd
import math
from PIL import Image, ImageDraw
import pandas as pd

def determine_looking_at(df, x, y):
    """
    Determines what the person is looking at based on given coordinates (x, y).
    
    Args:
    df (DataFrame): DataFrame containing bounding box information (x_min, x_max, y_min, y_max) and class names.
    x (float): X-coordinate of the point to check.
    y (float): Y-coordinate of the point to check.
    
    Returns:
    str: Class name if found within the bounding boxes, else 'Unknown'.
    """
    for index, row in df.iterrows():
        if row['x_min'] <= x <= row['x_max'] and row['y_min'] <= y <= row['y_max']:
            return row['Class Name']
    return "Unknown"

def extract_movie_lines(file_path, start_row=0):
    """
    Extracts the movie start time from a file starting from a specific row.
    
    Args:
    file_path (str): Path to the file to be read.
    start_row (int): Row number from which to start reading (default is 69).
    
    Returns:
    int: Movie start time if found, else None.
    """
    movie_start_time = None

    with open(file_path, 'r') as file:
        # Skip rows until the specified start row
        for _ in range(start_row - 1):
            next(file)

        # Now process the file from the start_row onwards
        for line in file:
            if "MovieStart" in line:
                parts = line.split()
                if len(parts) >= 2:
                    movie_start_time = int(parts[1])
                    break  # Stop after finding the movie start time
    return movie_start_time

def extract_efix_lines(file_path):
    """
    Extracts EFIX lines from the given file.
    
    Args:
    file_path (str): Path to the file to be read.
    
    Returns:
    list: List of EFIX lines.
    """
    with open(file_path, 'r') as file:
        efix_lines = [line for line in file if line.startswith("EFIX")]
    return efix_lines

def process_efix_lines_to_dataframe(efix_lines):
    """
    Processes the EFIX lines into a DataFrame, with specific columns renamed.
    
    Args:
    efix_lines (list): List of EFIX lines.
    
    Returns:
    DataFrame: Processed DataFrame with numeric columns and specific names.
    """
    parsed_lines = [line.strip().split()[2:] for line in efix_lines]  # Skip the first two elements ("EFIX R")
    
    # Create a DataFrame with dynamically generated column names
    columns = [f"col{i+1}" for i in range(len(parsed_lines[0]))]
    df = pd.DataFrame(parsed_lines, columns=columns)
    
    # Rename specific columns
    df.rename(columns={"col2": "end_time", "col1": "start_time", "col3": "duration", "col4": "x", "col5": "y"}, inplace=True)
    
    # Convert relevant columns to numeric
    df['start_time'] = pd.to_numeric(df['start_time'], errors='coerce')
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce')
    df['x'] = pd.to_numeric(df['x'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    print(df)
    # Count the number of duplicates
    num_duplicates = df.duplicated(subset='start_time', keep='first').sum()

    # Iterate over the DataFrame and update the start time for duplicates
    for idx in range(1, len(df)):
        if df.loc[idx, 'start_time'] == df.loc[idx - 1, 'start_time']:
            # Set the start time of the duplicate to the end time of the previous row
            df.loc[idx, 'start_time'] = df.loc[idx - 1, 'end_time']

    print(f'Number of duplicates: {num_duplicates}')
    
    # Sort the DataFrame by start_time in ascending order
    df.sort_values(by='start_time', ascending=True, inplace=True)
    
    return df

def calculate_fixation_frame(df, movie_start_time, output_file_path):
    """
    Iterates through the DataFrame to calculate the exact start time of fixation frames,
    writing the results to an output file.
    
    Args:
    df (DataFrame): DataFrame containing fixation data.
    movie_start_time (int): Movie start time for calculating exact start times.
    output_file_path (str): Path to output the result file.
    """
    with open(output_file_path, 'w') as f:
        for idx, row in df.iterrows():
            start_idx = row['start_time']
            exact_start = start_idx - movie_start_time
            
            if exact_start >= 0:
                # Write the exact start to the output file
                f.write(f"{str(exact_start)}\n")
            else:
                print(f"Negative result at index {idx}, row dropped.")
    
    print("Fixation data processing complete.")

def extract_efixations(file_path, output_file_path):
    """
    Main function to execute the processing steps: extracting movie start time,
    processing EFIX lines into DataFrame, and calculating fixation frames.
    
    Args:
    file_path (str): Path to the input file.
    output_file_path (str): Path to the output file where fixation frame results will be saved.
    """
    # Step 1: Extract movie start time
    movie_start_time = extract_movie_lines(file_path)
    
    if movie_start_time is None:
        print("Movie start time not found.")
        return

    # Step 2: Extract EFIX lines
    efix_lines = extract_efix_lines(file_path)
    
    if not efix_lines:
        print("No EFIX lines found.")
        return

    # Step 3: Process EFIX lines into a DataFrame
    df = process_efix_lines_to_dataframe(efix_lines)
    
    # Step 4: Calculate fixation frame based on movie start time
    calculate_fixation_frame(df, movie_start_time, output_file_path)

# Replace these with your specific file paths
file_path = '/path/your_eyetracking_data.asc'  # Replace with your file path
output_file_path = '/path/fixations_output.txt'  # Replace with your output file path

# Optional: Movie start time in milliseconds
movie_start_time = 12000  # Replace with your movie start time or None to skip adjustment

# Run extraction
extract_efixations(file_path, output_file_path, movie_start_time)