import os
from PIL import Image

SOURCE_FOLDER = './input_images'
OUTPUT_FOLDER = './output_images'
TARGET_FORMAT = 'PNG'  # Can be JPEG, PNG, WEBP
MAX_WIDTH = 800

def process_images():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for filename in os.listdir(SOURCE_FOLDER):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            try:
                img_path = os.path.join(SOURCE_FOLDER, filename)
                with Image.open(img_path) as img:
                    # Calculate new height to maintain aspect ratio
                    width_percent = (MAX_WIDTH / float(img.size[0]))
                    new_height = int((float(img.size[1]) * float(width_percent)))
                    
                    # Resize
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    
                    # Save with new extension
                    base_name = os.path.splitext(filename)[0]
                    new_filename = f"{base_name}.{TARGET_FORMAT.lower()}"
                    img.save(os.path.join(OUTPUT_FOLDER, new_filename), TARGET_FORMAT)
                    
                    print(f"Processed: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    # Create dummy folder for testing if it doesn't exist
    if not os.path.exists(SOURCE_FOLDER):
        os.makedirs(SOURCE_FOLDER)
        print(f"Created {SOURCE_FOLDER}. Put images there and run again.")
    else:
        process_images()
