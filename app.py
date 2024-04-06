import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import importlib.metadata
import tkinter as tk
import sys
import subprocess


def get_installed_packages():
    return sorted(["%s==%s" % (i.name, i.version) for i in importlib.metadata.distributions()])

def relaunch_app():
    app.destroy()
    subprocess.Popen([sys.executable, __file__])

def stage_packages():
    staged_packages.clear()
    for var, package in zip(package_vars, installed_packages):
        if var.get():
            staged_packages.append(package)
    staged_packages_text.config(state=tk.NORMAL)
    staged_packages_text.delete(1.0, tk.END)
    staged_packages_text.insert(tk.END, '\n'.join(staged_packages))
    staged_packages_text.config(state=tk.DISABLED)

def remove_packages():
    removed_packages_count = 0
    for package in staged_packages:
        package_name = package.split('==')[0]
        result = subprocess.run(["pip3", "uninstall", package_name, "-y", "-q"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            removed_packages_count += 1
            print(f"Package uninstalled: {package_name}")
        else:
            print(f"Failed to uninstall package: {package_name}")
    CTkMessagebox(title="Packages Removed",icon="check", message=f"{removed_packages_count} packages removed successfully.")
    print("All done")

installed_packages = get_installed_packages()
staged_packages = []
package_vars = []

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("theme.json") 



class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Pip Remove")
        self.geometry("750x600")
        frame = ctk.CTkFrame(self) 
        frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        title_label = ctk.CTkLabel(frame, text="Check the packages to stage", font=("Helvetica", 18)) # Using ctk.CTkLabel
        title_label.pack(anchor='w')
        subtitle_label = ctk.CTkLabel(frame, text="When removing Python-related pages, please exercise caution as this may lead to complications within the Python environment. It is crucial to ensure that you are selecting the correct pages, as the process may be irreversible\n", font=("Helvetica", 12), wraplength=220, justify='left') # Using ctk.CTkLabel
        subtitle_label.pack(anchor='w')
        canvas = tk.Canvas(frame, background="#212121") 
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview) 

        scrollable_frame = ctk.CTkFrame(canvas,border_color="#212121") 
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Calculate the maximum checkbox width
        max_checkbox_width = max([len(package) for package in installed_packages]) * 10

        for package in installed_packages:
            var = tk.BooleanVar()
            package_vars.append(var)
            chk = ctk.CTkCheckBox(scrollable_frame, text=package, variable=var) # Using ctk.CTkCheckBox
            chk.pack(anchor='w')

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.config(width=max_checkbox_width)

        staged_frame = ctk.CTkFrame(self) 
        staged_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        global staged_packages_text
        staged_packages_text = tk.Text(staged_frame, wrap=tk.WORD, state=tk.DISABLED) 
        staged_packages_text.pack(fill=tk.BOTH, expand=True)
        stage_button = ctk.CTkButton(staged_frame, text="Stage", command=stage_packages) 
        stage_button.pack(side=ctk.LEFT, padx=10, pady=10)
        remove_button = ctk.CTkButton(staged_frame, text="Remove", command=remove_packages)
        remove_button.pack(side=ctk.LEFT, padx=10, pady=10)
        refresh_button = ctk.CTkButton(staged_frame, text="Relaunch", command=relaunch_app) 
        refresh_button.pack(side=ctk.LEFT, padx=10, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()