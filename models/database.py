import sqlite3
from.student import Student


class StudentDatabase:
    def __init__(self, db_name='students.db'):
        self.conn=sqlite3.connect(db_name)
        self.create_table()


        def create_table(self):
            with self.conn:
                self.conn.execute('''CREATE TABLE IF NOT EXISTS students
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                  name TEXT,
                                  lastname TEXT,
                                  grade1 REAL,
                                  grade2 REAL,
                                  average REAL
                                  )''')
                

        def save_studen(self, student):
            with self.conn:
                self.conn.execute('INSERT INTO students(name, lastnmae, grade1, grade2, average) VALUES(?, ?, ?, ?, ?)',
                (student.name,student.lastname,student.grade1,student.grade2,student.average))


        def fetch_all_students(self):
            cursor =self.conn.cursor()
            cursor.execute('SELECT * FROM students')
            return [Student(*row) for row in cursor.fetchall()]