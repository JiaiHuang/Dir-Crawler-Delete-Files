import os 
import pandas as pd
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Directory Crawler Deleter")
the_canvas = tk.Canvas(root, width = 800, height = 500, bg = 'lightsteelblue')
the_canvas.pack()


def getdir():
    global folder_path
    import_file_path_dir = filedialog.askdirectory()
    folder_path = import_file_path_dir
    the_canvas.create_text(400, 225, text = import_file_path_dir)

def getExcel():
    global df
    import_file_path_excel = filedialog.askopenfilename()
    df = pd.read_csv(import_file_path_excel)
    the_canvas.create_text(400, 175, text = import_file_path_excel)

def delete():
    for folderName, subfolders, filesnames in os.walk(folder_path):
        print("The current folder is %s" %(folderName))
        for index, row in df.iterrows():
            fileName = row[df.columns.values[0]]
            for name in filesnames:
                if name == fileName:
                    os.remove("%s/%s" %(folderName, fileName))
                    print("Removed %s/%s" %(folderName, fileName))


browseButton_dir = tk.Button(text="Import Directory", command = getdir)
browseButton_excel = tk.Button(text="Import Excel File", command = getExcel)
delete_btn = tk.Button(text="Delete Files", command = delete)

the_canvas.create_window(400, 150, window=browseButton_excel)
the_canvas.create_window(400, 200, window=browseButton_dir)
the_canvas.create_window(400, 325, window=delete_btn)


root.mainloop()