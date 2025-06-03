
# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# # Define the SVN link
# svn_link = "http://tpms.cypress.com/tpmslib/Char_CCD/PSOC/Projects/S22/Devices/Explorer/Char_data/s22iolib%20A0_PCHAR%20Data/PCHAR%20Data%20Summaries/"

# # Function to get all Excel file links from the SVN directory
# def get_excel_file_links(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         file_links = []
#         for link in soup.find_all('a'):
#             href = link.get('href')
#             if href and href.endswith('.xlsx'):
#                 file_links.append(url + href)
#         return file_links
#     else:
#         print("Failed to retrieve files from the SVN link.")
#         return []

# # Function to combine all sheets from Excel files
# def combine_excel_files(file_list):
#     combined_data = {}
#     first_file = True  # Flag to check if it's the first file

#     for file in file_list:
#         print(f"Processing file: {file}")
#         try:
#             xls = pd.ExcelFile(file)
#             for sheet_name in xls.sheet_names:
#                 print(f"  Reading sheet: {sheet_name}")
#                 df = xls.parse(sheet_name)

#                 if first_file:
#                     # Use the first two rows as headers for the combined file
#                     combined_data[sheet_name] = df
#                     first_file = False
#                 else:
#                     # Remove the first two rows and append the rest
#                     df = df.iloc[2:]  # Keep only rows from the 3rd onward
#                     combined_data[sheet_name] = pd.concat([combined_data[sheet_name], df], ignore_index=True)

#         except Exception as e:
#             print(f"Error processing file {file}: {e}")

#     # Create the output directory if it doesn't exist
#     output_dir = r"C:\Users\Prakash\Downloads\Combined excel files"
#     os.makedirs(output_dir, exist_ok=True)

#     # Create a new Excel writer
#     combined_file_path = os.path.join(output_dir, 'combined_excel_file.xlsx')

#     # Check if the file already exists and remove it if necessary
#     if os.path.exists(combined_file_path):
#         os.remove(combined_file_path)

#     # Write all sheets to the Excel file
#     with pd.ExcelWriter(combined_file_path) as writer:
#         for sheet_name, df in combined_data.items():
#             print(f"  Writing sheet: {sheet_name}")
#             df.to_excel(writer, sheet_name=sheet_name, index=False)

#     print(f"Combined Excel file saved at: {combined_file_path}")

# # Main execution
# if __name__ == "__main__":
#     excel_files = get_excel_file_links(svn_link)
#     if excel_files:
#         combine_excel_files(excel_files)
#     else:
#         print("No Excel files found at the provided SVN link.")








# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# # Define the SVN link
# svn_link = "http://tpms.cypress.com/tpmslib/Char_CCD/PSOC/Projects/S22/Devices/Explorer/Char_data/s22iolib%20A0_PCHAR%20Data/PCHAR%20Data%20Summaries/"

# # Function to get all Excel file links from the SVN directory
# def get_excel_file_links(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         file_links = []
#         for link in soup.find_all('a'):
#             href = link.get('href')
#             if href and href.endswith('.xlsx'):
#                 file_links.append(url + href)
#         return file_links
#     else:
#         print("Failed to retrieve files from the SVN link.")
#         return []

# # Function to combine all sheets from Excel files
# def combine_excel_files(file_list):
#     combined_data = {}
#     first_file = True  # Flag to check if it's the first file

#     for file in file_list:
#         print(f"Processing file: {file}")
#         try:
#             xls = pd.ExcelFile(file)
#             for sheet_name in xls.sheet_names:
#                 print(f"  Reading sheet: {sheet_name}")
#                 df = xls.parse(sheet_name)

#                 if first_file:
#                     # Use the first two rows as headers for the combined file
#                     combined_data[sheet_name] = df
#                 else:
#                     # Remove the first two rows and append the rest
#                     df = df.iloc[2:]  # Keep only rows from the 3rd onward
#                     if sheet_name in combined_data:
#                         combined_data[sheet_name] = pd.concat([combined_data[sheet_name], df], ignore_index=True)
#                     else:
#                         combined_data[sheet_name] = df

#             # After processing the first file, set the flag to False
#             first_file = False

#         except Exception as e:
#             print(f"Error processing file {file}: {e}")

#     # Create the output directory if it doesn't exist
#     output_dir = r"C:\Users\Prakash\Downloads\Combined excel files"
#     os.makedirs(output_dir, exist_ok=True)

#     # Create a new Excel writer
#     combined_file_path = os.path.join(output_dir, 'combined_excel_file.xlsx')

#     # Check if the file already exists and remove it if necessary
#     if os.path.exists(combined_file_path):
#         os.remove(combined_file_path)

#     # Write all sheets to the Excel file
#     with pd.ExcelWriter(combined_file_path) as writer:
#         for sheet_name, df in combined_data.items():
#             print(f"  Writing sheet: {sheet_name}")
#             df.to_excel(writer, sheet_name=sheet_name, index=False)

#     print(f"Combined Excel file saved at: {combined_file_path}")

# # Main execution
# if __name__ == "__main__":
#     excel_files = get_excel_file_links(svn_link)
#     if excel_files:
#         combine_excel_files(excel_files)
#     else:
#         print("No Excel files found at the provided SVN link.")







# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# # Define the SVN link
# svn_link = "http://tpms.cypress.com/tpmslib/Char_CCD/PSOC/Projects/S22/Devices/Explorer/Char_data/s22iolib%20A0_PCHAR%20Data/PCHAR%20Data%20Summaries/"

# # Function to get all Excel file links from the SVN directory
# def get_excel_file_links(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         file_links = []
#         for link in soup.find_all('a'):
#             href = link.get('href')
#             if href and href.endswith('.xlsx'):
#                 file_links.append(url + href)
#         return file_links
#     else:
#         print("Failed to retrieve files from the SVN link.")
#         return []

# # Function to combine all sheets from Excel files
# def combine_excel_files(file_list):
#     combined_data = {}
#     first_file = True  # Flag to check if it's the first file

#     for file in file_list:
#         print(f"Processing file: {file}")
#         try:
#             xls = pd.ExcelFile(file)
#             for sheet_name in xls.sheet_names:
#                 print(f"  Reading sheet: {sheet_name}")
#                 df = xls.parse(sheet_name)

#                 if first_file:
#                     # Use the first two rows as headers for the combined file
#                     combined_data[sheet_name] = df
#                 else:
#                     # Remove the first two rows and append the rest
#                     df = df.iloc[2:]  # Keep only rows from the 3rd onward
#                     if sheet_name in combined_data:
#                         combined_data[sheet_name] = pd.concat([combined_data[sheet_name], df], ignore_index=True)
#                     else:
#                         combined_data[sheet_name] = df

#             # After processing the first file, set the flag to False
#             first_file = False

#         except Exception as e:
#             print(f"Error processing file {file}: {e}")

#     # Create the output directory if it doesn't exist
#     output_dir = r"C:\Users\Prakash\Downloads\Combined excel files"
#     os.makedirs(output_dir, exist_ok=True)

#     # Create a new Excel writer
#     combined_file_path = os.path.join(output_dir, 'combined_excel_file.xlsx')

#     # Check if the file already exists and remove it if necessary
#     if os.path.exists(combined_file_path):
#         os.remove(combined_file_path)

#     # Define the column renaming mapping for the Summary sheet
#     column_rename_mapping = {
#         "Specification": "Spec_min",
#         "Unnamed: 7": "Spec_avg",
#         "Unnamed: 8": "Spec_max",
#         "Typical": "Typical_Min",
#         "Unnamed: 13": "Typical_Max",
#         "Unnamed: 12": "Typical_Avg",
#         "Unnamed: 14": "Typical_Stdev",
#         "FF": "FF_min",
#         "FS": "FS_min",
#         "SF": "SF_min",
#         "SS": "SS_min",
#         "Unnamed: 17": "FF_max",
#         "Unnamed: 19": "FS_max",
#         "Unnamed: 21": "SF_max",
#         "Unnamed: 23": "SS_max"
#     }

#     # Write all sheets to the Excel file
#     with pd.ExcelWriter(combined_file_path) as writer:
#         for sheet_name, df in combined_data.items():
#             print(f"  Writing sheet: {sheet_name}")
#             # Rename columns only for the Summary sheet
#             if sheet_name.lower() == "summary":
#                 df.rename(columns=column_rename_mapping, inplace=True)
#             df.to_excel(writer, sheet_name=sheet_name, index=False)

#     print(f"Combined Excel file saved at: {combined_file_path}")

# # Main execution
# if __name__ == "__main__":
#     excel_files = get_excel_file_links(svn_link)
#     if excel_files:
#         combine_excel_files(excel_files)
#     else:
#         print("No Excel files found at the provided SVN link.")









import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define the SVN link
svn_link = "http://tpms.cypress.com/tpmslib/Char_CCD/PSOC/Projects/S22/Devices/Explorer/Char_data/s22iolib%20A0_PCHAR%20Data/PCHAR%20Data%20Summaries/"

# Function to get all Excel file links from the SVN directory
def get_excel_file_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        file_links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.xlsx'):
                file_links.append(url + href)
        return file_links
    else:
        print("Failed to retrieve files from the SVN link.")
        return []

# Function to combine all sheets from Excel files
def combine_excel_files(file_list):
    combined_data = {}
    first_file = True  # Flag to check if it's the first file

    for file in file_list:
        print(f"Processing file: {file}")
        try:
            xls = pd.ExcelFile(file)
            for sheet_name in xls.sheet_names:
                print(f"  Reading sheet: {sheet_name}")
                df = xls.parse(sheet_name)

                if first_file:
                    # Use the first two rows as headers for the combined file
                    combined_data[sheet_name] = df
                else:
                    # Remove the first two rows and append the rest
                    df = df.iloc[2:]  # Keep only rows from the 3rd onward
                    if sheet_name in combined_data:
                        combined_data[sheet_name] = pd.concat([combined_data[sheet_name], df], ignore_index=True)
                    else:
                        combined_data[sheet_name] = df

            # After processing the first file, set the flag to False
            first_file = False

        except Exception as e:
            print(f"Error processing file {file}: {e}")

    # Create the output directory if it doesn't exist
    output_dir = r"C:\Users\Prakash\Downloads\Combined excel files"
    os.makedirs(output_dir, exist_ok=True)

    # Create a new Excel writer
    combined_file_path = os.path.join(output_dir, 'combined_excel_file.xlsx')

    # Check if the file already exists and remove it if necessary
    if os.path.exists(combined_file_path):
        os.remove(combined_file_path)

    # Define the column renaming mapping for the Summary sheet
    column_rename_mapping = {
        "Specification": "Spec_min",
        "Unnamed: 7": "Spec_avg",
        "Unnamed: 8": "Spec_max",
        "Typical": "Typical_Min",
        "Unnamed: 13": "Typical_Max",
        "Unnamed: 12": "Typical_Avg",
        "Unnamed: 14": "Typical_Stdev",
        "FF": "FF_min",
        "FS": "FS_min",
        "SF": "SF_min",
        "SS": "SS_min",
        "Unnamed: 17": "FF_max",
        "Unnamed: 19": "FS_max",
        "Unnamed: 21": "SF_max",
        "Unnamed: 23": "SS_max"
    }

    # Write all sheets to the Excel file
    with pd.ExcelWriter(combined_file_path) as writer:
        for sheet_name, df in combined_data.items():
            print(f"  Writing sheet: {sheet_name}")
            # Apply changes only to the Summary sheet
            if sheet_name.lower() == "summary":
                # Rename columns
                df.rename(columns=column_rename_mapping, inplace=True)
                # Remove the second row after renaming
                df = df.drop(index=1).reset_index(drop=True)
            # Write the DataFrame to the Excel file
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Combined Excel file saved at: {combined_file_path}")

# Main execution
if __name__ == "__main__":
    excel_files = get_excel_file_links(svn_link)
    if excel_files:
        combine_excel_files(excel_files)
    else:
        print("No Excel files found at the provided SVN link.")
