import os
import random
import string
import subprocess
from tkinter import Tk, filedialog, messagebox, HORIZONTAL, Scale, Button, Label, Toplevel, Entry

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def rename_files_in_folder(folder_path, string_length):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            new_name = random_string(string_length) + os.path.splitext(filename)[1]
            new_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_path)
            print(f'Renamed: {filename} to {new_name}')
    messagebox.showinfo("Success", "All files have been renamed successfully!")
    open_folder(folder_path)

def open_folder(folder_path):
    if os.name == 'nt':  # Windows
        os.startfile(folder_path)
    elif os.name == 'posix':  # macOS or Linux
        subprocess.call(['open', folder_path])
    else:  # Linux
        subprocess.call(['xdg-open', folder_path])

def choose_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        dir_entry.delete(0, "end")
        dir_entry.insert(0, folder_selected)
    else:
        print("No folder selected.")

def start_renaming():
    folder_selected = dir_entry.get()
    if folder_selected and os.path.isdir(folder_selected):
        string_length = slider.get()
        rename_files_in_folder(folder_selected, string_length)
    else:
        messagebox.showerror("Error", "Please select a valid directory.")

def on_closing():
    root.destroy()

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Hide the root window

    # Create a new window for the controls
    settings_window = Toplevel()
    settings_window.title("Set String Length")

    Label(settings_window, text="Select the folder and length of the random string:").pack(pady=10)

    # Directory selection
    dir_frame = Label(settings_window)
    dir_frame.pack(pady=5)
    dir_entry = Entry(dir_frame, width=50)
    dir_entry.pack(side="left", padx=5)
    Button(dir_frame, text="Choose Directory", command=choose_directory).pack(side="right", padx=5)

    slider = Scale(settings_window, from_=4, to=20, orient=HORIZONTAL)
    slider.set(8)  # Default value
    slider.pack(pady=10)

    Button(settings_window, text="Start Renaming", command=start_renaming).pack(pady=20)

    # Ensure program stops when the settings window is closed
    settings_window.protocol("WM_DELETE_WINDOW", on_closing)

    settings_window.mainloop()
