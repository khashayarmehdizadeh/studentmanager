import sqlite3
import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

# کلاس مدل برای دانش‌آموز
class Student:
    def __init__(self, student_id, name, lastname, grade1, grade2, average):
        self.student_id = student_id  # شناسه دانش‌آموز
        self.name = name  # نام دانش‌آموز
        self.lastname = lastname  # نام خانوادگی دانش‌آموز
        self.grade1 = grade1  # نمره اول
        self.grade2 = grade2  # نمره دوم
        self.average = average  # محاسبه میانگین نمرات

# کلاس برای مدیریت دیتابیس دانش‌آموزان
class StudentDatabase:
    def __init__(self, db_name='students.db'):
        self.conn = sqlite3.connect(db_name)  # اتصال به دیتابیس SQLite
        self.create_table()  # ایجاد جدول در دیتابیس

    def create_table(self):
        # ایجاد جدول دانش‌آموزان در صورت عدم وجود
        with self.conn:
            self.conn.execute('DROP TABLE IF EXISTS students')  # حذف جدول قبلی (برای تست و توسعه)
            self.conn.execute('''CREATE TABLE IF NOT EXISTS students
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, lastname TEXT, grade1 REAL, grade2 REAL, average REAL)''')

    def save_student(self, student):
        # ذخیره اطلاعات دانش‌آموز در جدول
        with self.conn:
            self.conn.execute('INSERT INTO students (name, lastname, grade1, grade2, average) VALUES (?, ?, ?, ?, ?)',
                             (student.name, student.lastname, student.grade1, student.grade2, student.average))

    def delete_student(self, student_id):
        # حذف دانش‌آموز بر اساس شناسه
        with self.conn:
            self.conn.execute('DELETE FROM students WHERE id = ?', (student_id,))

    def update_student(self, student):
        # به‌روزرسانی اطلاعات دانش‌آموز
        with self.conn:
            self.conn.execute('''UPDATE students 
                                 SET name = ?, lastname = ?, grade1 = ?, grade2 = ?, average = ? 
                                 WHERE id = ?''',
                             (student.name, student.lastname, student.grade1, student.grade2, student.average, student.student_id))

    def fetch_all_students(self):
        # دریافت تمامی اطلاعات دانش‌آموزان
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, lastname, grade1, grade2, average FROM students')
        return [Student(*row) for row in cursor.fetchall()]

# کلاس برای مدیریت رابط کاربری
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Information Management")  # عنوان پنجره اصلی
        self.root.geometry("800x600")  # تنظیم اندازه پنجره
        self.root.configure(bg="#e0f7fa")  # رنگ پس‌زمینه

        self.db = StudentDatabase()  # ایجاد اتصال به دیتابیس
        self.create_widgets()  # ایجاد ویجت‌ها
        self.load_data()  # بارگذاری داده‌ها در رابط کاربری

    def create_widgets(self):
        # ایجاد فرم ورودی اطلاعات دانش‌آموز
        self.input_frame = ttk.Frame(self.root, padding="20")
        self.input_frame.pack(pady=20)

        self.entry_name = tk.StringVar()
        self.entry_lastname = tk.StringVar()
        self.entry_grade1 = tk.StringVar()
        self.entry_grade2 = tk.StringVar()

        fields = ["First Name", "Last Name", "Grade 1", "Grade 2"]
        variables = [self.entry_name, self.entry_lastname, self.entry_grade1, self.entry_grade2]
        for i, field in enumerate(fields):
            label = ttk.Label(self.input_frame, text=field)  # ایجاد لیبل برای هر فیلد
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = ttk.Entry(self.input_frame, textvariable=variables[i])  # ایجاد ورودی متن برای هر فیلد
            entry.grid(row=i, column=1, padx=10, pady=5)

        # دکمه ذخیره اطلاعات دانش‌آموز
        save_button = ttk.Button(self.root, text="Save Student", command=self.save_student_info)
        save_button.pack(pady=10)

        # جدول نمایش اطلاعات دانش‌آموزان
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        columns = ("ID", "First Name", "Last Name", "Grade 1", "Grade 2", "Average")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)  # تنظیم عنوان ستون‌ها
            self.tree.column(col, anchor="center")  # تنظیم تراز ستون‌ها

        self.tree.pack(fill=tk.BOTH, expand=True)

        # ایجاد دکمه‌های مدیریت اطلاعات
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        del_button = ttk.Button(button_frame, text="Delete Student", command=self.delete_student)  # دکمه حذف
        del_button.grid(row=0, column=0, padx=10, pady=5)

        edit_button = ttk.Button(button_frame, text="Edit Student", command=self.edit_student)  # دکمه ویرایش
        edit_button.grid(row=0, column=1, padx=10, pady=5)

        compare_button = ttk.Button(button_frame, text="Compare Students", command=self.compare_students)  # دکمه مقایسه
        compare_button.grid(row=0, column=2, padx=10, pady=5)

        # دکمه‌های جدید برای مدیریت CSV
        csv_import_button = ttk.Button(button_frame, text="Import from CSV", command=self.import_from_csv)
        csv_import_button.grid(row=1, column=0, padx=10, pady=5)

        csv_export_button = ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        csv_export_button.grid(row=1, column=1, padx=10, pady=5)

    def load_data(self):
        # بارگذاری اطلاعات از دیتابیس به جدول
        for row in self.tree.get_children():
            self.tree.delete(row)

        for student in self.db.fetch_all_students():
            self.tree.insert("", tk.END, values=(student.student_id, student.name, student.lastname, student.grade1, student.grade2, student.average))

    def save_student_info(self):
        # ذخیره اطلاعات وارد شده در دیتابیس
        name = self.entry_name.get()
        lastname = self.entry_lastname.get()
        grade1 = self.entry_grade1.get()
        grade2 = self.entry_grade2.get()

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
        student = Student(None, name, lastname, grade1, grade2, average)
        self.db.save_student(student)
        self.load_data()
        messagebox.showinfo("Success", "Student information saved successfully!")

    def delete_student(self):
        # حذف دانش‌آموز انتخاب شده از جدول و دیتابیس
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a student to delete!")
            return
        
        for item in selected_item:
            student_id = self.tree.item(item)['values'][0]
            self.db.delete_student(student_id)
            self.tree.delete(item)
        messagebox.showinfo("Success", "Student deleted successfully!")

    def edit_student(self):
        # ویرایش اطلاعات دانش‌آموز انتخاب شده
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a student to edit!")
            return

        student_id = self.tree.item(selected_item[0])['values'][0]
        
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

            average = (new_grade1 + new_grade2) / 2
            student = Student(student_id, new_name, new_lastname, new_grade1, new_grade2, average)
            self.db.update_student(student)
            self.load_data()
            edit_window.destroy()
            messagebox.showinfo("Success", "Student updated successfully!")

        selected_data = self.tree.item(selected_item[0])['values']
        edit_window = tk.Toplevel(self.root)
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
            label = ttk.Label(edit_window, text=field)  # لیبل‌های فرم ویرایش
            label.pack(pady=5)
            entry = ttk.Entry(edit_window, textvariable=variables[i])  # ورودی‌های فرم ویرایش
            entry.pack(pady=5)

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_edit)  # دکمه ذخیره تغییرات
        save_button.pack(pady=20)

    def compare_students(self):
        # مقایسه نمرات دانش‌آموزان انتخاب شده
        selected_items = self.tree.selection()
        if len(selected_items) < 2:
            messagebox.showerror("Selection Error", "Please select at least two students to compare!")
            return

        names = []
        grades1 = []
        grades2 = []

        for item in selected_items:
            values = self.tree.item(item)['values']
            names.append(f"{values[1]} {values[2]}")
            grades1.append(values[3])
            grades2.append(values[4])

        # نمایش نمودار برای مقایسه نمرات
        plt.figure(figsize=(10, 5))
        width = 0.35  # عرض میله‌ها

        # موقعیت‌های میله‌ها
        x = range(len(names))
        x1 = [i - width/2 for i in x]
        x2 = [i + width/2 for i in x]

        # ایجاد میله‌ها برای هر نمره
        plt.bar(x1, grades1, width, label='نمره 1', color='blue')
        plt.bar(x2, grades2, width, label='نمره 2', color='orange')

        # افزودن عنوان‌ها و برچسب‌ها
        plt.xlabel('دانش‌آموزان')
        plt.ylabel('نمرات')
        plt.title('مقایسه نمرات دانش‌آموزان')
        plt.xticks(x, names, rotation=45)
        plt.legend()

        # نمایش نمودار
        plt.tight_layout()
        plt.show()

    def import_from_csv(self):
        # وارد کردن اطلاعات از فایل CSV به دیتابیس
        file_path = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # رد کردن سطر هدر
            for row in reader:
                if len(row) != 4:
                    continue
                name, lastname, grade1, grade2 = row
                try:
                    grade1 = float(grade1)
                    grade2 = float(grade2)
                except ValueError:
                    continue
                average = (grade1 + grade2) / 2
                student = Student(None, name, lastname, grade1, grade2, average)
                self.db.save_student(student)
        self.load_data()
        messagebox.showinfo("Success", "Data imported from CSV successfully!")

    def export_to_csv(self):
        # صادر کردن اطلاعات از دیتابیس به فایل CSV
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["First Name", "Last Name", "Grade 1", "Grade 2", "Average"])
            for student in self.db.fetch_all_students():
                writer.writerow([student.name, student.lastname, student.grade1, student.grade2, student.average])
        messagebox.showinfo("Success", "Data exported to CSV successfully!")

# اجرای برنامه
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()