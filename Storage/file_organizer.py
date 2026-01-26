import os
import shutil

# Define the directory to organize
TARGET_DIR = '/path/to/your/directory'  # CHANGE THIS

# Define the mapping of folder names to extensions
EXTENSIONS = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
    'Archives': ['.zip', '.rar', '.tar', '.gz'],
    'Audio': ['.mp3', '.wav', '.flac'],
    'Video': ['.mp4', '.mkv', '.mov', '.avi'],
    'Installers': ['.exe', '.msi', '.dmg', '.pkg']
}

def organize_files():
    if not os.path.exists(TARGET_DIR):
        print(f"The directory {TARGET_DIR} does not exist.")
        return

    for filename in os.listdir(TARGET_DIR):
        file_path = os.path.join(TARGET_DIR, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        moved = False
        _, ext = os.path.splitext(filename)
        
        for folder, extensions in EXTENSIONS.items():
            if ext.lower() in extensions:
                folder_path = os.path.join(TARGET_DIR, folder)
                os.makedirs(folder_path, exist_ok=True)
                shutil.move(file_path, os.path.join(folder_path, filename))
                print(f"Moved: {filename} -> {folder}/")
                moved = True
                break
        
        # Optional: Move unknown types to an 'Others' folder
        if not moved:
            other_path = os.path.join(TARGET_DIR, 'Others')
            os.makedirs(other_path, exist_ok=True)
            shutil.move(file_path, os.path.join(other_path, filename))
            print(f"Moved: {filename} -> Others/")

if __name__ == "__main__":
    organize_files()
