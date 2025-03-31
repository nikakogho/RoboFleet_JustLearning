import os

def aggregate_python_files(start_dir=".", exclude_folders = [], exclude_files = []):
    with open("aggregated.txt", "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk(start_dir):
            if len(exclude_folders) > 0:
                dirs[:] = [d for d in dirs if d not in exclude_folders]
            
            for file in files:
                if not file.endswith(".py") or file in exclude_files:
                    continue

                file_path = os.path.join(root, file)
                outfile.write(file_path + "\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        outfile.write(content + "\n")
                except Exception as e:
                    outfile.write(f"Error reading {file_path}: {e}\n")
                # Write three spaces as a separator and a newline.
                outfile.write("   \n")

if __name__ == "__main__":
    aggregate_python_files(exclude_folders=['.venv', 'venv'], exclude_files=['files_aggregator.py'])
