import os 
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import xlrd
from datetime import datetime

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
    df = pd.read_excel(import_file_path_excel)
    the_canvas.create_text(400, 175, text = import_file_path_excel)

def delete():
    dfSuccessLog = pd.DataFrame(columns = ["file name", "file path", "clickable url"])
    df_fail_log = pd.DataFrame(columns = ["file name", "error", "file path", "clickable url"])
    for folderName, subfolders, filesnames in os.walk(os.path.normpath(folder_path)):
        print("The current folder is %s" %(folderName))
        for index, row in df.iterrows():
            fileName = str(row[df.columns.values[0]])
            keep = str(row[df.columns.values[1]])
            for name in filesnames:
                if(pd.notna(fileName)):
                    fileName = (fileName.replace('%20', ' '))
                full_path = os.path.join(folderName, name)
                formatName = name.split(".")[0]
                if str(formatName).strip().lower() == str(fileName).strip().lower() and keep == 'N':
                    try:
                        os.remove(full_path)
                        new_row_success = {"file name": fileName, "file path": full_path, "clickable url": None}
                        dfSuccessLog = dfSuccessLog.append(new_row_success, ignore_index =True)
                        if df["Keep?"][index] == 'N':
                            index += 1
                            while pd.isna(df["Keep?"][index]) and pd.isna(df["File Title"][index]):
                                index+=1
                                new_row_url = {"file name": None, "file path": None, "clickable url": df["CLICKABLE URL"][index]}
                                dfSuccessLog = dfSuccessLog.append(new_row_url, ignore_index =True)
                        print("Removed %s" %(full_path))
                    except:
                        print("Error while deleting file, %s" %(full_path))
                        new_row_fail = {"file name": fileName, "error": "Error while deleing file, %s" %(full_path), "file path": full_path, "clickable url": None}
                        df_fail_log = df_fail_log.append(new_row_fail, ignore_index =True)
    print("Finished, please close the application")
    if(not df_fail_log.empty):
        df_fail_log.to_excel(datetime.now().strftime("%y-%m-%d_%H-%M-%S") + "_" + "deleteFailLog.xlsx")

    dfSuccessLog.to_excel(datetime.now().strftime("%y-%m-%d_%H-%M-%S") + "_" + "deleteSuccussLog.xlsx")


browseButton_dir = tk.Button(text="Import Directory", command = getdir)
browseButton_excel = tk.Button(text="Import excel File", command = getExcel)
delete_btn = tk.Button(text="Delete Files", command = delete)

the_canvas.create_window(400, 150, window=browseButton_excel)
the_canvas.create_window(400, 200, window=browseButton_dir)
the_canvas.create_window(400, 325, window=delete_btn)


root.mainloop()
