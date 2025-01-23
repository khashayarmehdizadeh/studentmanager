import sqlite3
from models.student import Student

class DatabaseManager:
    def __init__(self, db_name='students.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS students
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, lastname TEXT, grade1 REAL, grade2 REAL, average REAL)''')

    def add_student(self, student):
        with self.conn:
            self.conn.execute('INSERT INTO students (name, lastname, grade1, grade2, average) VALUES (?, ?, ?, ?, ?)',
                              (student.name, student.lastname, student.grade1, student.grade2, student.average))

    def update_student(self, student):
        with self.conn:
            self.conn.execute('''UPDATE students 
                                 SET name = ?, lastname = ?, grade1 = ?, grade2 = ?, average = ?
                                 WHERE id = ?''',
                              (student.name, student.lastname, student.grade1, student.grade2, student.average, student.student_id))

    def delete_student(self, student_id):
        with self.conn:
            self.conn.execute('DELETE FROM students WHERE id = ?', (student_id,))

    def fetch_all_students(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students')
        return [Student(*row) for row in cursor.fetchall()]
