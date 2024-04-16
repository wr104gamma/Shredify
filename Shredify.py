#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shredify v1.0")
        self.root.geometry("400x300")
        
        # Create menu
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        self.cascade_items = []  # Keep track of cascade items
        
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Add Files", command=self.add_files)
        self.file_menu.add_command(label="Add Directories", command=self.add_directories)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.cascade_items.append(self.file_menu)  # Add to cascade items
        
        # About menu
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="Instructions", command=self.show_instructions)
        self.cascade_items.append(self.about_menu)  # Add to cascade items

        # Shred menu (aligned to the right)
        self.shred_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Shred", menu=self.shred_menu)
        self.passes_var = tk.IntVar(value=3)
        self.shred_menu.add_radiobutton(label="2 Pass", variable=self.passes_var, value=1)
        self.shred_menu.add_radiobutton(label="4 Passes", variable=self.passes_var, value=3)
        self.shred_menu.add_radiobutton(label="6 Passes", variable=self.passes_var, value=5)
        self.shred_menu.add_radiobutton(label="8 Passes", variable=self.passes_var, value=7)
        self.shred_menu.add_radiobutton(label="10 Passes", variable=self.passes_var, value=9)
        self.shred_menu.add_command(label="Shred Selected Files", command=self.shred_selected_files)
        self.cascade_items.append(self.shred_menu)  # Add to cascade items
        
        # Create a listbox to display files
        self.file_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, font=("Arial", 12))  # Set font size here
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display message for pasting path and filenames
        self.file_listbox.insert(tk.END, "Paste your path/filename(s) Here")
        self.file_listbox.itemconfig(0, {'fg': 'black'})  # Change text color
        
        # Add horizontal scrollbar
        scrollbar_x = tk.Scrollbar(root, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.file_listbox.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.config(command=self.file_listbox.xview)
        
        # Enable right-click context menu
        self.file_listbox.bind("<Button-3>", self.right_click_menu)
        
        # Enable Ctrl-V for pasting
        self.root.bind("<Control-v>", self.paste_files)

    def add_files(self):
        # Open a file dialog to select files
        files = filedialog.askopenfilenames(title="Select Files", filetypes=(("All files", "*.*"),))
        if files:
            # Add selected files to the listbox
            for file in files:
                self.file_listbox.insert(tk.END, file)
        
    def add_directories(self):
        # Open a custom directory dialog to select directories
        directory = filedialog.askdirectory(parent=self.root, title="Select Directory")
        if directory:
            # Add all files from the selected directory to the listbox
            files = []
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    self.file_listbox.insert(tk.END, file_path)
                    files.append(file_path)
                    
            # Automatically select the newly added files
            for file in files:
                idx = self.file_listbox.get(0, tk.END).index(file)
                self.file_listbox.selection_set(idx)

    def show_instructions(self):
        # Create a new window for instructions
        about_window = tk.Toplevel(self.root)
        about_window.title("About Shredifier")
        
        # Instructions text
        instructions_text = ("Shredifier v1.0 Is Free To Use and Open Source.\n"
                             "Shredifier uses the 'shred' command-line interface with the (-v -n -z -u functions).\n"
                             "Larger files and batches of files may take longer to process.\n"
                             "You can paste paths/filenames for shredding by pressing Ctrl-V.\n"
                             "If you have any questions or suggestions, please email")
        instructions_label = tk.Label(about_window, text=instructions_text, wraplength=700, justify="center")
        instructions_label.pack(padx=10, pady=10)
        
        # Create hyperlink for email
        email_link = tk.Label(about_window, text="wr104gamma@gmail.com", fg="blue", cursor="hand2")
        email_link.pack()
        email_link.bind("<Button-1>", lambda e: self.open_email())

    def open_email(self):
        subprocess.Popen(["xdg-open", "mailto:wr104gamma@gmail.com"])

    def remove_selected_files(self):
        # Get the selected files
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            # Remove selected files from the listbox
            for idx in reversed(selected_indices):  # Iterate in reverse order to avoid index shifting
                self.file_listbox.delete(idx)

    def shred_selected_files(self):
        # Get the selected files
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            # Prompt the user once before shredding all files
            response = messagebox.askyesno("Confirm Shredding", "Are you sure you want to shred all selected files?")
            if response:
                success_count = 0
                failure_count = 0
                files_to_delete = []  # List to store files to delete from the listbox
                # Shred each selected file
                for idx in selected_indices:
                    file = self.file_listbox.get(idx)
                    # Exclude the instruction message from shredding
                    if file != "Paste your path/filename(s) Here":
                        command = f"sudo shred -v -n {self.passes_var.get()} -z -u '{file}'"
                        try:
                            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            success_count += 1
                            files_to_delete.append(idx)  # Add the index to files_to_delete list
                        except subprocess.CalledProcessError as e:
                            failure_count += 1

                # Remove the shredded files from the listbox
                for idx in reversed(files_to_delete):  # Iterate in reverse order to avoid index shifting
                    self.file_listbox.delete(idx)
                # Display the result of the batch operation
                if success_count > 0:
                    messagebox.showinfo("Batch Shredding", f"Successfully shredded {success_count} file(s).")
                if failure_count > 0:
                    messagebox.showerror("Batch Shredding", f"Failed to shred {failure_count} file(s).")
        else:
            # Display a message if no files are selected
            messagebox.showwarning("No Files Selected", "Please select one or more files to shred.")

    def paste_files(self, event=None):
        # Get the clipboard data
        clipboard_data = self.root.clipboard_get()
        # Check if the clipboard contains file paths
        if clipboard_data:
            # Split clipboard data by newlines
            files = clipboard_data.splitlines()
            # Add files to the listbox
            for file in files:
                # Insert the file into the listbox
                self.file_listbox.insert(tk.END, file)
                # Highlight and select the newly added file
                idx = self.file_listbox.size() - 1
                self.file_listbox.selection_set(idx)

    def right_click_menu(self, event):
        # Create a right-click context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Paste", command=self.paste_files)
        context_menu.add_command(label="Remove", command=self.remove_selected_files)
        context_menu.tk_popup(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()
