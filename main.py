import tkinter
import tkinter.messagebox
import customtkinter
import sys
import os
import subprocess
import time
import threading
from tkinter import simpledialog, Toplevel, Radiobutton, StringVar

# Calling external classes and functions
from geometry_constructor import GeometryConstructor 

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    WIDTH = 1680
    HEIGHT = 920

    def __init__(self):
        super().__init__()

        self.title("SplashFlows")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.geometry("+0+0")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # App is made of 4 columns
        self.grid_columnconfigure(1, weight=1)
        # App is made of 3 rows
        self.grid_rowconfigure(0, weight=1)

        self.frame_left()
        self.frame_middle_top()
        self.frame_middle_bottom()
        self.frame_right()
        self.frame_right_bottom()
    
    def frame_left(self):
        self.frame_left = customtkinter.CTkFrame(master=self)
        self.frame_left.grid(row=0, column=0, rowspan=2, sticky="nswe", ipady=20)
        
        # Create a label widget
        self.ltitle_frame = customtkinter.CTkFrame(master=self.frame_left, width=300, height=40)
        self.ltitle_frame.grid(row=0, column=0, sticky="we", padx=15, pady=15)
        self.ltitle_frame.grid_propagate(False)
        self.ltitle = customtkinter.CTkLabel(master=self.ltitle_frame, text="SplashFlows")
        self.ltitle.place(relx=0.5, rely=0.5, anchor="center")
        self.ltitle.configure(font=("Roboto Medium", 20))

        # Case Types and Test Cases Selection
        self.case_type_combobox = customtkinter.CTkComboBox(master=self.frame_left, values=["Hybrid_Les_Rans", "Laminar", "Les", "Rans", "Swarm", "Vof"], command=self.update_test_cases)
        self.case_type_combobox.grid(row=1, column=0, pady=10, padx=20, sticky="we")
        self.case_type_combobox.set("Select Simulation Type") # Set the simulation type at the start 
        
        self.test_case_combobox = customtkinter.CTkComboBox(master=self.frame_left, values=["Select Case"])
        self.test_case_combobox.grid(row=2, column=0, pady=10, padx=20, sticky="we")
        self.test_case_combobox.set("Select Case")  # Set the default item as the selected value

        self.load_case_button = customtkinter.CTkButton(master=self.frame_left, text="Load Case", command=self.load_case)
        self.load_case_button.grid(row=3, column=0, pady=10, padx=20, sticky="we")
        
        # Initialize the variable to store the selected case path
        self.selected_case_path = None
        #-------------------------------------------< 
         
        # Add Construct Geometry button 
        ##self.construct_geometry_button = customtkinter.CTkButton(master=self.frame_left, text="Construct Geometry", command=self.construct_geometry)
        self.construct_geometry_button = customtkinter.CTkButton(master=self.frame_left, text="Construct Geometry", command=self.activate_geometry_constructor)
        self.construct_geometry_button.grid(row=4, column=0, pady=10, padx=20, sticky="we")

        # Add Generate Mesh button
        self.generate_mesh_button = customtkinter.CTkButton(master=self.frame_left, text="Generate Mesh", command=self.generate_mesh)
        self.generate_mesh_button.grid(row=5, column=0, pady=10, padx=20, sticky="we")

        # Add Run Case button
        self.run_case_button = customtkinter.CTkButton(master=self.frame_left, text="Run Case", command=self.run_case)
        self.run_case_button.grid(row=6, column=0, pady=10, padx=20, sticky="we")

        self.frame_left.grid_rowconfigure(7, weight=1)

        # Initialize the parameters for T-Flows sub-programs
        self.process_check_var = tkinter.IntVar(value=0)
        self.generate_check_var = tkinter.IntVar(value=0)
        self.divide_check_var = tkinter.IntVar(value=0)
        self.convert_check_var = tkinter.IntVar(value=0)

        # Configuration of the compile button and T-Flows pillers
        self.compile_button = customtkinter.CTkButton(master=self.frame_left, text="Compile Code", command=self.compile_code, fg_color="cyan", text_color="black", hover_color="white", font=("Roboto Medium",16))
        self.compile_button.grid(row=8, column=0, pady=10, padx=20, sticky="we") # Compile the selected T-Flows sub-programs
        # T-Flows pillers
        self.process_checkbox = customtkinter.CTkCheckBox(master=self.frame_left, text="Process", variable=self.process_check_var)
        self.process_checkbox.grid(row=9, column=0, pady=10, padx=20, sticky="we")
        self.generate_checkbox = customtkinter.CTkCheckBox(master=self.frame_left, text="Generate", variable=self.generate_check_var)
        self.generate_checkbox.grid(row=10, column=0, pady=10, padx=20, sticky="we")
        self.divide_checkbox = customtkinter.CTkCheckBox(master=self.frame_left, text="Divide", variable=self.divide_check_var)
        self.divide_checkbox.grid(row=11, column=0, pady=10, padx=20, sticky="we")
        self.convert_checkbox = customtkinter.CTkCheckBox(master=self.frame_left, text="Convert", variable=self.convert_check_var)
        self.convert_checkbox.grid(row=12, column=0, pady=10, padx=20, sticky="we")       

    def frame_middle_top(self):
        # Create the Text widget within the new frame (text box)
        self.output_text = tkinter.Text(master=self, height=30, width=90, bg="black", fg="white", wrap=tkinter.WORD)
        self.output_text.grid(row=0, column=1, sticky="nsew", padx=(20,0), pady=(20,0))
        self.output_text.tag_configure("cyan_text", foreground="cyan") # Configure a tag for cyan-colored text

        # Insert the default welcome message at the beginning
        ascii_art_message = """
=======================================================================
   __          __    _                                  _             
   \ \        / /   | |                                | |            
    \ \  /\  / /___ | |  ___  ___   _ __ ___    ___    | |_   ___      
     \ \/  \/ // _ \| | / __|/ _ \ | '_ ` _ \  / _ \   | __| / _ \     
      \  /\  /|  __/| || (__| (_) || | | | | ||  __/   | |_ | (_) |    
       \/  \/  \___||_| \___|\___/ |_| |_| |_| \___|    \__| \___/     
   _____         _              _      ______  _                      
  / ____|       | |            | |    |  ____|| |                     
 | (___   _ __  | |  __ _  ___ | |__  | |__   | |  ___  __      __ ___ 
  \___ \ | '_ \ | | / _` |/ __|| '_ \ |  __|  | | / _ \ \ \ /\ / // __|
  ____) || |_) || || (_| |\__ \| | | || |     | || (_) | \ V  V / \__ \\
 |_____/ | .__/ |_| \__,_||___/|_| |_||_|     |_| \___/   \_/\_/  |___/
         | |                ___    __     ___                         
         |_|               / _ \  /_ |   / _ \                        
                  __   __ | | | |  | |  | | | |                       
                  \ \ / / | | | |  | |  | | | |                       
                   \ V /  | |_| |_ | | _| |_| |                       
                    \_/    \___/(_)|_|(_)\___/                        
                    
                       GUI tool for T-Flows 
                    © 2024 SplashFlows v0.1.0
=======================================================================                                       
        """ 
        self.output_text.insert("1.0", ascii_art_message)
        # Apply the "cyan_text" tag to the entire message
        self.output_text.tag_add("cyan_text", "1.0", "end")

        # Create and place the scrollbar next to the Text widget
        self.output_scrollbar = tkinter.Scrollbar(master=self, width=15, command=self.output_text.yview)
        self.output_scrollbar.grid(row=0, column=2, sticky='nsw', pady=(20,0))
        self.output_text.config(yscrollcommand=self.output_scrollbar.set)

    def frame_middle_bottom(self):
        self.frame_middle_bottom = customtkinter.CTkFrame(master=self)
        self.frame_middle_bottom.grid(row=1, column=1, columnspan=2, sticky="nswe", padx=(20, 0), pady=20)
        
        self.mbtitle_frame = customtkinter.CTkFrame(master=self.frame_middle_bottom, width=900, height=40)
        self.mbtitle_frame.grid(row=0, column=0, columnspan=3, sticky="we", padx=15, pady=15)
        self.mbtitle_frame.grid_propagate(False)
        self.mbtitle = customtkinter.CTkLabel(master=self.mbtitle_frame, text="Controls")
        self.mbtitle.place(relx=0.5, rely=0.5, anchor="center")
        self.mbtitle.configure(font=("Roboto Medium", 20))

        # Place the save button below the Text widget
        self.entry_label = customtkinter.CTkLabel(master=self.frame_middle_bottom, text="Working Directory:", anchor="w")
        self.entry_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="we")
        self.entry = customtkinter.CTkEntry(master=self.frame_middle_bottom, placeholder_text="Select working directory...") # Case Types and Test Cases Selection
        self.entry.grid(row=1, column=1, pady=10, padx=20, sticky="we")
        self.save_button = customtkinter.CTkButton(master=self.frame_middle_bottom, text="Open Folder") # Add command to open folder
        self.save_button.grid(row=1, column=2, pady=10, padx=20, sticky="we")
        self.save_button = customtkinter.CTkButton(master=self.frame_middle_bottom, text="Save Changes", command=self.save_dom_file)
        self.save_button.grid(row=2, column=2, pady=10, padx=20, sticky="we")
        segemented_button = customtkinter.CTkSegmentedButton(master=self.frame_middle_bottom, values=["Clear all changes", "Undo last change", "Dsicard changes"]) #, command=segmented_button_callback)
        segemented_button.grid(row=2, column=1, pady=10, padx=20, sticky="we")
        #segemented_button.set("Value 1")

    def frame_right(self):
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=3, sticky="nswe", padx=20, pady=(20, 0))

        self.rtitle_frame = customtkinter.CTkFrame(master=self.frame_right, width=300, height=40)
        self.rtitle_frame.grid(row=0, column=0, sticky="we", padx=15, pady=15)
        self.rtitle_frame.grid_propagate(False)
        self.rtitle = customtkinter.CTkLabel(master=self.rtitle_frame, text="Post-Processing")
        self.rtitle.place(relx=0.5, rely=0.5, anchor="center")
        self.rtitle.configure(font=("Roboto Medium", 20))
        
        # ========================= Progress bar + Slider ====================================
        # Create a container frame for the progress bar and slider
        self.overlay_frame = customtkinter.CTkFrame(master=self.frame_right, width=300, height=80)
        self.overlay_frame.grid(row=1, column=0, sticky="we", padx=15, pady=15)
        self.overlay_frame.grid_propagate(False)

        # Add the progress bar to the container frame
        self.progressbar = customtkinter.CTkProgressBar(master=self.overlay_frame)
        self.progressbar.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.9)
        self.progressbar.set(0.5)

        # Add percentage label
        self.progress_percentage_label = customtkinter.CTkLabel(master=self.overlay_frame, text="50%")
        self.progress_percentage_label.place(relx=0.5, rely=0.3, anchor="center")

        # Add the slider to the same container frame, slightly below the progress bar
        self.slider_2 = customtkinter.CTkSlider(master=self.overlay_frame, command=self.update_progress)
        self.slider_2.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.9)
        # Initialize the progress bar value somewhere appropriate in your code
        self.slider_2.set(0.5)  # Initial slider position to match progress bar

        self.button_5 = customtkinter.CTkButton(master=self.frame_right, text="Execute", command=self.execute_command)
        self.button_5.grid(row=2, column=0, columnspan=1, pady=20, padx=20, sticky="we")

    def frame_right_bottom(self):
        self.frame_right_bottom = customtkinter.CTkFrame(master=self)
        self.frame_right_bottom.grid(row=1, column=3, sticky="nswe", padx=20, pady=20)

        self.overlay_frame_1 = customtkinter.CTkFrame(master=self.frame_right_bottom, width=300, height=40)
        self.overlay_frame_1.grid(row=0, column=0, sticky="we", padx=15, pady=15)
        self.overlay_frame_1.grid_propagate(False)
        self.settings_label = customtkinter.CTkLabel(master=self.overlay_frame_1, text="Settings")
        self.settings_label.place(relx=0.5, rely=0.5, anchor="center")
        self.settings_label.configure(font=("Roboto Medium", 20))

        # Scaling option
        self.scaling_label = customtkinter.CTkLabel(self.frame_right_bottom, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=1, column=0, padx=20, pady=(10, 0),sticky="we")
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.frame_right_bottom, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 20),sticky="we")
        self.scaling_optionemenu.set("100%")

        # Switch for changing program theme
        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_right_bottom, text="Dark Mode", command=self.change_mode)
        self.switch_2.grid(row=3, column=0, pady=10, padx=20, sticky="we")
        self.switch_2.select()

        # Initialize the timer parameters
        self.start_time = time.time()
        self.elapsed_time_label = customtkinter.CTkLabel(master=self.frame_right_bottom, text="Elapsed Time: 00:00:00", font=("Roboto Medium", 14))
        self.elapsed_time_label.grid(row=4, column=0, sticky="we", padx=20, pady=10)
        # Call the timer function to start counting the time 
        self.update_elapsed_time()
           
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    def activate_geometry_constructor(self):
        # This method can activate the GeometryConstructor
        self.geometry_constructor = GeometryConstructor(self)
        # You might want to call a method from GeometryConstructor here if needed
        
    def update_progress(self, value):
        # Assuming value is between 0 and 1
        self.progressbar.set(value)
        percentage_text = f"{int(value * 100)}%"
        #self.progress_percentage_label.configure(fg_color="cyan")
        self.progress_percentage_label.configure(text=percentage_text)
        
    # ------------------------- Template cases of T-Flows --------------------------
    # Test cases - types and benchmarks     
    def update_test_cases(self, event=None):
        case_type = self.case_type_combobox.get()
        if case_type == "Select Simulation Type":
            self.test_case_combobox.configure(values=["Select Case"])
            self.test_case_combobox.set("Select Case")
            return

        test_cases_directory = f"../Tests/{case_type}"
        try:
            test_cases = [name for name in os.listdir(test_cases_directory) if os.path.isdir(os.path.join(test_cases_directory, name))]
        except FileNotFoundError:
            test_cases = []
            print(f"Directory not found: {test_cases_directory}")

        test_cases.insert(0, "Select Case")  # Ensure the placeholder is at the start
        self.test_case_combobox.configure(values=test_cases)
        self.test_case_combobox.set("Select Case")
        
        
    def load_case(self):
        case_type = self.case_type_combobox.get()
        test_case = self.test_case_combobox.get()

        if case_type == "Select Simulation Type" or test_case == "Select Case":
            tkinter.messagebox.showinfo("Error", "Please select a case type and test case.")
            return

        case_path = os.path.abspath(f"../Tests/{case_type}/{test_case}")  # Use absolute path
        sub_cases = [name for name in os.listdir(case_path) if os.path.isdir(os.path.join(case_path, name))]

        if sub_cases:
            self.show_sub_cases_popup(case_path, sub_cases)
        else:
            self.selected_case_path = case_path
            print(f"Loading case from: {self.selected_case_path}")
            self.display_dom_file_content()
            print(f"Displaying the domain file content")
            # Call the method to create soft links for executable files in the Binaries directory
            self.create_soft_links()

    def show_sub_cases_popup(self, case_path, sub_cases):
        popup = Toplevel(self.master)
        popup.title("Select Sub-Case")
        popup.geometry("300x200")

        selected_sub_case = StringVar(value=sub_cases[0])
        for sub_case in sub_cases:
            Radiobutton(popup, text=sub_case, variable=selected_sub_case, value=sub_case).pack(anchor=tkinter.W)

        def on_submit():
            final_case_path = os.path.abspath(os.path.join(case_path, selected_sub_case.get()))  # Use absolute path
            self.selected_case_path = final_case_path
            print(f"Selected sub-case: {self.selected_case_path}")
            popup.destroy()
            self.display_dom_file_content()
            self.create_soft_links()

        submit_button = customtkinter.CTkButton(popup, text="Submit", command=on_submit)
        submit_button.pack(pady=10)
            
    def display_dom_file_content(self):
        self.dom_file_name = None  # Reset or declare this variable
        dom_files = [file for file in os.listdir(self.selected_case_path) if file.endswith('.dom')]
        if dom_files:
            self.dom_file_name = dom_files[0]  # Store the .dom file name
            dom_file_path = os.path.join(self.selected_case_path, self.dom_file_name)
            with open(dom_file_path, 'r') as file:
                dom_content = file.read()
            self.output_text.delete(1.0, tkinter.END)
            self.output_text.insert(tkinter.END, dom_content)
        else:
            self.output_text.delete(1.0, tkinter.END)
            self.output_text.insert(tkinter.END, "No .dom file found in the selected case directory.")
            
    def save_dom_file(self):
        if self.selected_case_path and self.dom_file_name:  # Ensure a case and .dom file are selected
            dom_file_path = os.path.join(self.selected_case_path, self.dom_file_name)
            with open(dom_file_path, 'w') as file:
                file_content = self.output_text.get("1.0", tkinter.END)
                file.write(file_content)
            tkinter.messagebox.showinfo("Success", "The file has been successfully saved.")
        else:
            tkinter.messagebox.showerror("Error", "No .dom file is selected or available to save.")
            
    def create_soft_links(self):
        binaries_path = os.path.abspath("../Binaries")  # Path to the Binaries directory
        target_dir = self.selected_case_path  # Target directory where links will be created

        # Check if the Binaries directory exists
        if not os.path.exists(binaries_path):
            print("Binaries directory does not exist. Skipping link creation.")
            return

        # Iterate over each file in the Binaries directory
        for item in os.listdir(binaries_path):
            source_path = os.path.join(binaries_path, item)
            link_path = os.path.join(target_dir, item)

            # Check if the item is a file and is executable
            if os.path.isfile(source_path) and os.access(source_path, os.X_OK):
                # Check if the link already exists, if not, create a symbolic link
                if not os.path.exists(link_path):
                    try:
                        os.symlink(source_path, link_path)
                        print(f"Link created for {item}")
                    except Exception as e:
                        print(f"Error creating link for {item}: {e}")
                else:
                    print(f"Link already exists for {item}")
    # ------------------------- Template cases of T-Flows --------------------------

    def execute_command(self):
        # Retrieve the command from the entry widget
        command = self.entry.get()
        if not command:  # Fallback if the entry is empty, use the placeholder or a default command
            command = "top"
        
        # Platform-specific logic to open a terminal and run the command
        if sys.platform.startswith('linux'):
            # For Linux, using gnome-terminal as an example
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
        elif sys.platform.startswith('win32'):
            # For Windows
            subprocess.Popen(['cmd', '/c', command])
        elif sys.platform.startswith('darwin'):
            # For macOS
            subprocess.Popen(['open', '-a', 'Terminal', command])
        else:
            print(f"Unsupported platform: {sys.platform}")    
            
    def compile_code(self):
        self.output_text.delete('1.0', tkinter.END)  # Clear the Text widget at the start

        # Initialize or reset compilation flags for each sub-program
        self.compiled_flags = {
            "Process": False,
            "Generate": False,
            "Divide": False,
            "Convert": False,
        }

        subprograms = {
            "Process": self.process_check_var,
            "Generate": self.generate_check_var,
            "Divide": self.divide_check_var,
            "Convert": self.convert_check_var,
        }
        selected_subprograms = {name: var.get() for name, var in subprograms.items() if var.get() == 1}

        if not any(selected_subprograms.values()):
            tkinter.messagebox.showerror("Error", "No choice was detected, please choose the part of the code you want to compile.")
            return

        compile_success = True  # Flag to track overall compilation success
        base_path = "../Sources"
        for subprogram, selected in selected_subprograms.items():
            if selected:
                subprogram_path = f"{base_path}/{subprogram}"
                try:
                    process = subprocess.Popen(["make", "-C", subprogram_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                    for line in iter(process.stdout.readline, ''):
                        self.output_text.insert(tkinter.END, line)
                        self.output_text.see(tkinter.END)
                        self.update_idletasks()
                    process.wait()
                    if process.returncode != 0:
                        tkinter.messagebox.showerror("Compilation Error", f"Failed to compile {subprogram}.")
                        compile_success = False
                        break
                    else:
                        # Update the compilation flag for this sub-program
                        self.compiled_flags[subprogram] = True
                except Exception as e:
                    tkinter.messagebox.showerror("Compilation Error", f"Failed to compile {subprogram}. Error: {e}")
                    compile_success = False
                    break

        if compile_success:
            self.output_text.insert(tkinter.END, "Compilation successful for all selected subprograms!")
         
    def construct_geometry(self):
        print("Constructing Geometry...")

    def generate_mesh(self):
        print("Generating Mesh...")

    def run_case(self):
        print("Running Case...")
    
    def update_elapsed_time(self):
        elapsed_time = int(time.time() - self.start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Update the label's text to show the elapsed time in a HH:MM:SS format
        self.elapsed_time_label.configure(text=f"Elapsed Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
        # Schedule the next update call to this method after 1000ms (1 second)
        self.after(1000, self.update_elapsed_time)
        
    def button_event(self):
        print("Button pressed")

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
