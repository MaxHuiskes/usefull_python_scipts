import os
from PyPDF2 import PdfMerger

SOURCE_DIR = './pdfs_to_merge'
OUTPUT_FILE = 'merged_document.pdf'

def merge_pdfs():
    merger = PdfMerger()
    
    # Get all PDF files and sort them
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.pdf')]
    files.sort()

    if not files:
        print("No PDF files found in the directory.")
        return

    print(f"Merging {len(files)} files...")
    
    for pdf in files:
        path = os.path.join(SOURCE_DIR, pdf)
        merger.append(path)
        print(f"Appended: {pdf}")

    merger.write(OUTPUT_FILE)
    merger.close()
    print(f"Successfully created: {OUTPUT_FILE}")

if __name__ == "__main__":
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
        print(f"Created {SOURCE_DIR}. Place PDFs here and run the script.")
    else:
        merge_pdfs()
