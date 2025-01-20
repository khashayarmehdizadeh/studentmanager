import sqlite3
import csv
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from tkinter import ttk

# ایجاد دیتابیس و جدول برای ذخیره‌سازی اطلاعات
def create_database():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS students')
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (name TEXT, lastname TEXT, grade1 REAL, grade2 REAL, average REAL)''')
    conn.commit()
    conn.close()

# ذخیره اطلاعات در دیتابیس
def save_to_database(name, lastname, grade1, grade2, average):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('INSERT INTO students (name, lastname, grade1, grade2, average) VALUES (?, ?, ?, ?, ?)',
              (name, lastname, grade1, grade2, average))
    conn.commit()
    conn.close()

# ذخیره اطلاعات در فایل CSV
def save_to_csv(name, lastname, grade1, grade2, average):
    with open('students.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, lastname, grade1, grade2, average])

# بارگذاری داده‌ها از فایل CSV
def load_from_csv():
    with open('students.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            save_to_database(*row)

# ذخیره اطلاعات در دیتابیس و فایل CSV
def save_student_info():
    name = entry_name.get()
    lastname = entry_lastname.get()
    grade1 = entry_grade1.get()
    grade2 = entry_grade2.get()

    if not name or not lastname or not grade1 or not grade2:
        messagebox.showerror("Input Error", "All fields must be filled!")
        return

    try:
        grade1 = float(grade1)
        grade2 = float(grade2)
    except ValueError:
        messagebox.showerror("Input Error", "Grades must be numbers!")
        return

    if not (0 <= grade1 <= 20 and 0 <= grade2 <= 20):
        messagebox.showerror("Input Error", "Grades must be between 0 and 20!")
        return

    average = (grade1 + grade2) / 2
    save_to_database(name, lastname, grade1, grade2, average)
    save_to_csv(name, lastname, grade1, grade2, average)
    update_student_table()
    messagebox.showinfo("Success", "Student information saved successfully!")

# جستجو برای دانش‌آموز
def search_student():
    search_term = search_var.get().lower()
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT name, lastname, grade1, grade2, average FROM students')
    rows = c.fetchall()
    for row in rows:
        if search_term in row[0].lower() or search_term in row[1].lower():
            tree.insert("", tk.END, values=row)
    conn.close()

# نمایش نمودار عملکرد دانش‌آموز
def show_performance_chart():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to view their performance!")
        return
    for selected_item in selected_item:
        name, lastname, grade1, grade2, _=tree.item(selected_item)['values']
        plt.figure()
        plt.bar(['Grade 1','Grade 2'], [grade1,grade2])
        plt.title(f'Performance of {name} {lastname}')
        plt.xlabel('subjects')
        plt.ylabel('Grades')
        plt.show()

# به‌روزرسانی جدول دانش‌آموزان
def update_student_table():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT name, lastname, grade1, grade2, average FROM students')
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# ایجاد پنجره گرافیکی
window = tk.Tk()
window.title("Student Information")
window.geometry("800x600")
window.configure(bg="#e0f7fa")

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#4caf50", foreground="white")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

input_frame = tk.Frame(window, bg="#ffffff", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
input_frame.pack(pady=10)

# متغیرهای ورودی به‌صورت جداگانه
entry_name = tk.StringVar()
entry_lastname = tk.StringVar()
entry_grade1 = tk.StringVar()
entry_grade2 = tk.StringVar()

fields = ["First Name", "Last Name", "Grade 1", "Grade 2"]
for i, field in enumerate(fields):
    label = tk.Label(input_frame, text=field, bg="#ffffff", font=('Arial', 12))
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(input_frame, textvariable=[entry_name, entry_lastname, entry_grade1, entry_grade2][i], font=('Arial', 12))
    entry.grid(row=i, column=1, padx=10, pady=5)

# دکمه‌های مختلف
save_button = tk.Button(window, text="Save Information", command=save_student_info, bg="#4caf50", fg="white", font=('Arial', 12), width=20)
save_button.pack(pady=10)

search_var = tk.StringVar()
search_entry = tk.Entry(window, textvariable=search_var, font=('Arial', 12))
search_entry.pack(pady=10)
search_button = tk.Button(window, text="Search", command=search_student, bg="#2196f3", fg="white", font=('Arial', 12), width=20)
search_button.pack(pady=10)

performance_button = tk.Button(window, text="Show Performance Chart", command=show_performance_chart, bg="#ff9800", fg="white", font=('Arial', 12), width=20)
performance_button.pack(pady=10)

# جدول اطلاعات
tree_frame = tk.Frame(window)
tree_frame.pack(pady=20)

columns = ("Name", "Last Name", "Grade 1", "Grade 2", "Average")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

tree.pack()

# شروع برنامه
create_database()
load_from_csv()
update_student_table()
window.mainloop()