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
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, lastname TEXT, grade1 REAL, grade2 REAL, average REAL)''')
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
    try:
        with open('students.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                save_to_database(*row)
    except FileNotFoundError:
        pass

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

# حذف دانش‌آموز انتخاب‌شده
def delete_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to delete!")
        return
    
    for item in selected_item:
        student_id = tree.item(item)['values'][0]
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        tree.delete(item)
    messagebox.showinfo("Success", "Student deleted successfully!")

# ویرایش اطلاعات دانش‌آموز انتخاب‌شده
def edit_student():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a student to edit!")
        return

    student_id = tree.item(selected_item[0])['values'][0]
    
    def save_edit():
        new_name = edit_name.get()
        new_lastname = edit_lastname.get()
        new_grade1 = edit_grade1.get()
        new_grade2 = edit_grade2.get()

        try:
            new_grade1 = float(new_grade1)
            new_grade2 = float(new_grade2)
        except ValueError:
            messagebox.showerror("Input Error", "Grades must be numbers!")
            return

        if not (0 <= new_grade1 <= 20 and 0 <= new_grade2 <= 20):
            messagebox.showerror("Input Error", "Grades must be between 0 and 20!")
            return

        new_average = (new_grade1 + new_grade2) / 2
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('''UPDATE students 
                     SET name = ?, lastname = ?, grade1 = ?, grade2 = ?, average = ? 
                     WHERE id = ?''',
                  (new_name, new_lastname, new_grade1, new_grade2, new_average, student_id))
        conn.commit()
        conn.close()
        update_student_table()
        edit_window.destroy()
        messagebox.showinfo("Success", "Student updated successfully!")

    selected_data = tree.item(selected_item[0])['values']
    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Student")
    edit_window.geometry("400x300")
    edit_window.configure(bg="#f0f0f0")

    edit_name = tk.StringVar(value=selected_data[1])
    edit_lastname = tk.StringVar(value=selected_data[2])
    edit_grade1 = tk.StringVar(value=selected_data[3])
    edit_grade2 = tk.StringVar(value=selected_data[4])

    fields = ["First Name", "Last Name", "Grade 1", "Grade 2"]
    variables = [edit_name, edit_lastname, edit_grade1, edit_grade2]
    for i, field in enumerate(fields):
        label = tk.Label(edit_window, text=field, bg="#f0f0f0", font=('Arial', 12))
        label.pack(pady=5)
        entry = tk.Entry(edit_window, textvariable=variables[i], font=('Arial', 12))
        entry.pack(pady=5)

    save_button = tk.Button(edit_window, text="Save Changes", command=save_edit, bg="#4CAF50", fg="white", font=('Arial', 12))
    save_button.pack(pady=20)

# مقایسه دانش‌آموزان انتخاب‌شده
def compare_students():
    selected_items = tree.selection()
    if len(selected_items) < 2:
        messagebox.showerror("Selection Error", "Please select at least two students to compare!")
        return

    names = []
    grades1 = []
    grades2 = []

    for item in selected_items:
        values = tree.item(item)['values']
        names.append(f"{values[1]} {values[2]}")
        grades1.append(values[3])
        grades2.append(values[4])

    x = range(len(names))
    plt.figure(figsize=(8, 5))
    plt.bar(x, grades1, width=0.4, label='Grade 1', align='center')
    plt.bar([p + 0.4 for p in x], grades2, width=0.4, label='Grade 2', align='center')
    plt.xticks([p + 0.2 for p in x], names, rotation=30)
    plt.xlabel('Students')
    plt.ylabel('Grades')
    plt.title('Comparison of Students')
    plt.legend()
    plt.tight_layout()
    plt.show()

# به‌روزرسانی جدول دانش‌آموزان
def update_student_table():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# ایجاد پنجره گرافیکی
window = tk.Tk()
window.title("Student Information Management")
window.geometry("1000x700")
window.configure(bg="#e0f7fa")

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#4CAF50", foreground="white")
style.configure("Treeview", font=('Arial', 10), rowheight=25)

# ورودی‌ها
input_frame = tk.Frame(window, bg="#ffffff", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
input_frame.pack(pady=20)

entry_name = tk.StringVar()
entry_lastname = tk.StringVar()
entry_grade1 = tk.StringVar()
entry_grade2 = tk.StringVar()

fields = ["First Name", "Last Name", "Grade 1", "Grade 2"]
variables = [entry_name, entry_lastname, entry_grade1, entry_grade2]
for i, field in enumerate(fields):
    label = tk.Label(input_frame, text=field, bg="#ffffff", font=('Arial', 12))
    label.grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(input_frame, textvariable=variables[i], font=('Arial', 12))
    entry.grid(row=i, column=1, padx=10, pady=5)

save_button = tk.Button(window, text="Save Student", command=save_student_info, bg="#4CAF50", fg="white", font=('Arial', 12))
save_button.pack(pady=10)

# جدول اطلاعات
tree_frame = tk.Frame(window, bg="#e0f7fa")
tree_frame.pack(pady=20, fill=tk.BOTH, expand=True)

columns = ("ID", "First Name", "Last Name", "Grade 1", "Grade 2", "Average")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill=tk.BOTH, expand=True)




# دکمه‌های عملیاتی
button_frame = tk.Frame(window, bg="#e0f7fa")
button_frame.pack(pady=20)

del_button = tk.Button(button_frame, text="Delete Student", command=delete_student, bg="#F44336", fg="white", font=('Arial', 12))
del_button.grid(row=0, column=0, padx=10, pady=5)

edit_button = tk.Button(button_frame, text="Edit Student", command=edit_student, bg="#2196F3", fg="white", font=('Arial', 12))
edit_button.grid(row=0, column=1, padx=10, pady=5)

compare_button = tk.Button(button_frame, text="Compare Students", command=compare_students, bg="#FF9800", fg="white", font=('Arial', 12))
compare_button.grid(row=0, column=2, padx=10, pady=5)

# شروع برنامه
create_database()
load_from_csv()
update_student_table()
window.mainloop()