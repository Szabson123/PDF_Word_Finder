import tkinter as tk
from tkinter import filedialog
import os
from multiprocessing import Pool, freeze_support
import fitz 

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

def search_for_flag_in_pdfs(folder_path, word):
    if not os.path.exists(folder_path):
        return f"Folder not found: {folder_path}"

    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]

    with Pool() as pool:
        results = pool.map(find_word_in_pdf, [(file_path, word) for file_path in file_paths])

    return results

def filter_files():
    folder_path = path_entry.get()
    word = word_entry.get()
    
    root.after(100, run_search, folder_path, word)

def run_search(folder_path, word):
    results = search_for_flag_in_pdfs(folder_path, word)
    display_results(results, word)

def display_results(results, word):
    result_text.delete(1.0, tk.END)
    for result in results:
        if result is not None:
            file_path, outcome = result
            if isinstance(outcome, int):
                result_text.insert(tk.END, f"'{word}' found in {file_path} on page {outcome}\n")
            else:
                result_text.insert(tk.END, f"{file_path}: {outcome}\n")
                
                
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)

def setup_gui():
    global root, path_entry, word_entry, result_text

    root = tk.Tk()
    root.title("PDF Word Finder")

    # Path entry
    tk.Label(root, text="Folder Path:").grid(row=0, column=0, sticky="w")
    path_entry = tk.Entry(root, width=50)
    path_entry.grid(row=0, column=1, sticky="we")
    browse_button = tk.Button(root, text="Browse", command=browse_folder)
    browse_button.grid(row=0, column=2, sticky="we")

    # Word entry
    tk.Label(root, text="Word to Find:").grid(row=1, column=0, sticky="w")
    word_entry = tk.Entry(root)
    word_entry.grid(row=1, column=1, sticky="we")

    # Filter button
    filter_button = tk.Button(root, text="Filter", command=filter_files)
    filter_button.grid(row=2, column=0, columnspan=3, sticky="we")

    # Result area
    result_text = tk.Text(root, height=10)
    result_text.grid(row=3, column=0, columnspan=3, sticky="nsew")

    # Start the GUI event loop
    root.mainloop()

if __name__ == '__main__':
    freeze_support()
    setup_gui()