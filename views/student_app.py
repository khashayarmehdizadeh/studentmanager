import tkinter as tk
from tkinter import ttk
from models.database import StudentDatabase



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
        
        fields =["First Name","Last Name","Grade 1","Grade 2"]
        variables =[self.entry_name,self.entry_lastname,self.entry_grade1,self.entry_grade2]
        for i, field in enumerate(fields):
            lable=ttk.Label(self.input_frame,text=field)
            lable.grid(row=i,column=0,padx=10,pady=5)
            entry=ttk.Entry(self.input_frame,textvariable=variables[i])
            entry.grid(row=i,column=1,padx=10,pady=5)

        save_button=ttk.Button(self.root,text="Save",command=self.save_student_info)
        save_button.pack(pady=10)

        self.tree_frame=ttk.Frame(self.root)
        self.tree_frame.pack(pady=10,fill=tk.BOTH,expand=True)

        columns=("ID","First Name","Last Neme","Grade 1","Grade 2","Average")
        self.tree=ttk.Treeview(self.tree_frame,columns=columns,show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col,anchor="center")

        self.tree.pack(fill=tk.BOTH,expand=True)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        

        for student in self.db.fetch_all_students():
            self.tree.insert("",tk.END,values=(student.student_id,student.name,student.lastname,student.grade1,student.grade2,student.average))

    
    def save_student_info(self):
        name=self.entry_name.get()
        lastname=self.entry_lastname.get()
        grade1=self.entry_grade1.get()
        grade2=self.entry_grade2.get()



        if not name or not lastname or not grade1 or not grade2:
            tk.messagebox.showerror("Incorrect","All fields must be filled!")
            return
        try:
            grade1=float(grade1)
            grade2=float(grade2)
        except ValueError:
            tk.messagebox.showerror("Errorr","Grades must be numbers")
            return
        

        if not( 0<=grade1 <= 20 and 0<= grade2 <=20):
            tk.messagebox.showerror("Error","Grades must be between 0 and 20!")
            return
        
        average=(grade1+grade2)/2
        student=Student(None, name, lastname, grade1, grade2)
        student.average=average
        self.db.save_student(student)
        self.load_data()
        tk.messagebox.showinfo("Success","Student information saved successfully")