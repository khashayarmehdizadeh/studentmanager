import tkinter as tk
from tkinter import ttk
from..models.database import StudentDatabase


class StudentApp:
    def __init__(self, root):
        self.root=root
        self.root.title("Student Information Managment")
        self.root.geometry("800x600")
        self.db=StudentDatabase()
        self.create_widgets()
        self.load_data()


    def create_widgets(self):
        self.input_frame=ttk.Frame(self.root, padding="20")
        self.input_frame.pack(pady=20)

        self.entry_name=tk.StringVar()
        self.entry_lastname=tk.StringVar()
        self.entry_grade1=tk.StringVar()
        self.entry_grade2=tk.StringVar()
        
        fields =["Fi"]

        