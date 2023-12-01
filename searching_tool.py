import os
from PyPDF2 import PdfReader
 
def find_word_in_pdf(file_path, word):
    word = word.lower()  
    try:
        reader = PdfReader(file_path)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text().lower()  
            if word in text:
                return page_num  # Zwraca numer strony zamiast True
        return None
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None
 
def search_for_flag_in_pdfs(folder_path, word):
    print(f"Searching for '{word}' in PDF files in {folder_path}...")
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return
 
    pdf_files_found = False
 
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_files_found = True
            file_path = os.path.join(folder_path, filename)
            page_num = find_word_in_pdf(file_path, word)
            if page_num is not None:
                print(f"'{word}' found in {filename} on page {page_num}")
 
    if not pdf_files_found:
        print("No PDF files found in the folder.")


search_for_flag_in_pdfs(r'C:\\Users\\szaba\\Desktop\\PDF_Finder', 'flag')
