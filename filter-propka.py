import argparse
import os
import pandas as pd
import re

# Set display options to show all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def read_data(file_path):
    start_marker = "SUMMARY OF THIS PREDICTION"
    stop_keyword = "---------"
    data = []

    with open(file_path, 'r') as file:
        found_marker = False
        for line in file:
            if not found_marker:
                if line.strip() == start_marker:
                    found_marker = True
            elif stop_keyword in line:
                break
            else:
                # Split line into columns using multiple spaces as delimiter
                columns = re.split(r'\s+', line.strip())
                # Keep only the first 4 columns, ignore the rest
                data.append(columns[:4])

    return data
    
def filter_dataframe(df, pka_threshold, resname_value=None, chain_value=None, output_file=None):
    with open(output_file, 'w') as output:
        residues_to_filter = ['ASP', 'GLU', 'HIS', 'LYS']
        if resname_value:
            residues_to_filter = [resname_value]

        for res in residues_to_filter:
            if res in ['ASP', 'GLU', 'HIS']:
                direction = '>'
                filtered_df = df[(df['Resname'] == res) & (df['pKa'].astype(float) > pka_threshold)]
            elif res == 'LYS':
                direction = '<'
                filtered_df = df[(df['Resname'] == res) & (df['pKa'].astype(float) < pka_threshold)]
            else:
                output.write(f"Unrecognized residue: {res}\n")
                continue

            if chain_value:
                filtered_df = filtered_df[filtered_df['Chain'] == chain_value]

            output.write(f"{res}: pKa {direction} {pka_threshold}\n")
            output.write(f"{filtered_df}\n")
            output.write("-----------\n")

    return filtered_df

def main():
    parser = argparse.ArgumentParser(description="Filter pKa data from a PROPKA output file.")
    parser.add_argument("file_path", help="Path to the PROPKA output file")
    parser.add_argument("pka_threshold", type=float, help="Threshold for pKa filtering, i.e. pH")
    parser.add_argument("--resname_value", help="Resname value to filter (ASP, GLU, HIS, LYS)")
    parser.add_argument("--chain_value", help="Chain value to filter")
    args = parser.parse_args()

    # Check if the provided file has a .pka extension
    if not args.file_path.lower().endswith('.pka'):
        print("Error: Input file must have a .pka extension")
        return

    # Generate the output file name with pka_threshold, resname_value, and chain_value
    output_name_parts = os.path.splitext(os.path.basename(args.file_path))[0]
    if args.resname_value:
        output_name_parts += f"_pH{args.pka_threshold:.0f}_{args.resname_value}"
    else:
        output_name_parts += f"_pH{args.pka_threshold:.0f}"

    if args.chain_value:
        output_name_parts += f"_{args.chain_value}"

    output_name_parts += ".out"
    output_file_name = output_name_parts

    # Read the data and create the original DataFrame
    column_names = ["Resname", "Resid", "Chain", "pKa"]
    data = read_data(args.file_path)

    df = pd.DataFrame(data, columns=column_names)

    # Remove the first row (header) and the last column
    df = df.iloc[1:]

    # Call the function to filter the DataFrame for specified resname_value and chain_value
    filtered_df = filter_dataframe(df, args.pka_threshold, args.resname_value, args.chain_value, output_file=output_file_name)


if __name__ == "__main__":
    main()
