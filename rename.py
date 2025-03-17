import os

def rename_files(directory, base_name, start_number):
    files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.pdf')], key=lambda x: int(''.join(filter(str.isdigit, x))), reverse=False)  # Sort in ascending order based on numerical values
    
    for file in files:
        old_path = os.path.join(directory, file)
        new_name = f"{base_name}-{str(start_number).zfill(4)}.pdf"
        new_path = os.path.join(directory, new_name)
        
        if os.path.isfile(old_path):  # Ensure it's a file before renaming
            os.rename(old_path, new_path)
            print(f"Renamed: {file} -> {new_name}")
        
        start_number += 1  # Increment to maintain ascending order

# Example usage
directory = "DEC 2017 CA OBR"  # Change this to your folder path
base_name = "CA-MOOE-2017-12"
start_number = 131 # Change this to your desired starting number
rename_files(directory, base_name, start_number)