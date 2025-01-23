import tkinter as tk
from tkinter import ttk, messagebox
from utils.chart import display_comparison_chart

class StudentView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Student Management")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.entry_name = tk.StringVar()
        self.entry_lastname = tk.StringVar()
        self.entry_grade1 = tk.StringVar()
        self.entry_grade2 = tk.StringVar()

        # Input fields
        fields = [("First Name", self.entry_name), ("Last Name", self.entry_lastname), 
                  ("Grade 1", self.entry_grade1), ("Grade 2", self.entry_grade2)]
        for i, (label, var) in enumerate(fields):
            ttk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5)
            ttk.Entry(self.root, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

        # Buttons
        ttk.Button(self.root, text="Add Student", command=self.add_student).grid(row=4, column=0, pady=10)
        ttk.Button(self.root, text="Compare Students", command=self.compare_students).grid(row=4, column=1, pady=10)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "First Name", "Last Name", "Grade 1", "Grade 2", "Average"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.grid(row=5, column=0, columnspan=2, pady=10)

    def add_student(self):
        name, lastname = self.entry_name.get(), self.entry_lastname.get()
        grade1, grade2 = self.entry_grade1.get(), self.entry_grade2.get()
        success, message = self.controller.add_student(name, lastname, grade1, grade2)
        if success:
            self.refresh_tree()
        messagebox.showinfo("Info", message)

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for student in self.controller.get_all_students():
            self.tree.insert("", tk.END, values=(student.student_id, student.name, student.lastname, student.grade1, student.grade2, student.average))

    def compare_students(self):
        selected_items = self.tree.selection()
        if len(selected_items) < 2:
            messagebox.showerror("Error", "Select at least two students!")
            return
        students = [self.tree.item(item)["values"] for item in selected_items]
        display_comparison_chart(students)

    def run(self):
        self.refresh_tree()
        self.root.mainloop()
