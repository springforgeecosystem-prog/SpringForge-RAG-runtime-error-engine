import json
import glob

def merge_files():
    # 1. Find all files ending in .json
    files = glob.glob('*.json')
    
    merged_list = []
    count = 0
    
    print(f"Found {len(files)} JSON files. Starting merge...")

    for filename in files:
        # Avoid reading the output file if it already exists
        if filename == 'merged_master.json':
            continue
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # If the file contains a list of items, add them all
                if isinstance(data, list):
                    merged_list.extend(data)
                    count += len(data)
                # If the file is a single item, add it to the list
                else:
                    merged_list.append(data)
                    count += 1
                    
                print(f" -> Merged: {filename}")
                
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # 2. Save the result to a new file
    with open('merged_master.json', 'w', encoding='utf-8') as outfile:
        # indent=4 makes it readable; remove it if you want a smaller file size
        json.dump(merged_list, outfile, indent=4)
    
    print(f"\nSuccess! Merged {count} records into 'merged_master.json'.")

if __name__ == "__main__":
    merge_files()