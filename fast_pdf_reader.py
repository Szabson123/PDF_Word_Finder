import os
from PyPDF2 import PdfReader
from multiprocessing import Pool
import fitz  # PyMuPDF
import time

def find_word_in_pdf(args):
    file_path, word = args
    try:
        with fitz.open(file_path) as doc:
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                if word.lower() in text.lower():
                    return file_path, page_num + 1
    except Exception as e:
        return file_path, f"Error: {e}"

def search_for_flag_in_pdfs(folder_path, word, processes=None):
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        return

    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]

    with Pool(processes=processes) as pool:
        results = pool.map(find_word_in_pdf, [(file_path, word) for file_path in file_paths])

    for result in results:
        if result is not None:
            file_path, outcome = result
            if isinstance(outcome, int):
                print(f"'{word}' found in {file_path} on page {outcome}")
            else:
                print(f"{file_path}: {outcome}")
                
                
if __name__ == '__main__':
    start_time = time.time()
    search_for_flag_in_pdfs(r'C:\\Users\\szaba\\Desktop\\PDF_Finder', 'flag')
    elapsed_time = time.time() - start_time
    print(f"Czas wykonania całego skryptu: {elapsed_time} sekund")

    
