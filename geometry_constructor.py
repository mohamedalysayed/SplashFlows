import tkinter as tk
from tkinter import simpledialog
import vtk

class GeometryConstructor:
    def __init__(self, master):
        self.master = master
        self.master.geometry('200x50')
        self.button = tk.Button(master, text='Construct Geometry', command=self.construct_geometry)
        self.button.grid(sticky="ew")  # Using grid instead of pack

    def construct_geometry(self):
        print("Constructing Geometry...")
        
        length = simpledialog.askfloat("Input", "Length of the channel:", parent=self.master)
        width = simpledialog.askfloat("Input", "Width of the channel:", parent=self.master)
        height = simpledialog.askfloat("Input", "Height of the channel:", parent=self.master)

        if length is None or width is None or height is None:
            print("Geometry construction canceled.")
            return

        # Here you can add the code to construct the geometry and save it in VTK format.
        # I'll add a simple print statement for demonstration.
        print(f"Channel dimensions: Length={length}, Width={width}, Height={height}")

        # Example: creating and saving a rectangular channel in VTK format.
        # You would replace this with the actual code that uses the 'vtk' library.
        self.save_geometry_to_vtk(length, width, height)

    def save_geometry_to_vtk(self, length, width, height):
        # Dummy function to mimic VTK file saving
        print("Saving geometry to VTK format...")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryConstructor(root)
    root.mainloop()
