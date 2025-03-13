import pandas as pd

def csv_to_markdown(csv_file, md_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Replace NaN values with a space
    df = df.fillna(' ')

    # Convert the DataFrame to a Markdown table
    md_table = df.to_markdown(index=False)

    # Write the Markdown table to a file
    with open(md_file, 'w') as f:
        f.write(md_table)

if __name__ == "__main__":
    csv_file = 'implementations/compatibility_hardware.csv'
    md_file = 'implementations/_compatibility_hardware.md'
    csv_to_markdown(csv_file, md_file)
    print(f"Markdown table has been written to {md_file}")
    
    csv_file = 'implementations/compatibility_software.csv'
    md_file = 'implementations/_compatibility_software.md'
    csv_to_markdown(csv_file, md_file)
    print(f"Markdown table has been written to {md_file}")