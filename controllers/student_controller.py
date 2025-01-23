from models.student import Student
from database.database_manager import DatabaseManager

class StudentController:
    def __init__(self):
        self.db = DatabaseManager()

    def add_student(self, name, lastname, grade1, grade2):
        try:
            grade1, grade2 = float(grade1), float(grade2)
            if 0 <= grade1 <= 20 and 0 <= grade2 <= 20:
                student = Student(None, name, lastname, grade1, grade2)
                self.db.add_student(student)
                return True, "Student added successfully!"
            else:
                return False, "Grades must be between 0 and 20!"
        except ValueError:
            return False, "Grades must be numbers!"

    def update_student(self, student_id, name, lastname, grade1, grade2):
        try:
            grade1, grade2 = float(grade1), float(grade2)
            if 0 <= grade1 <= 20 and 0 <= grade2 <= 20:
                student = Student(student_id, name, lastname, grade1, grade2)
                self.db.update_student(student)
                return True, "Student updated successfully!"
            else:
                return False, "Grades must be between 0 and 20!"
        except ValueError:
            return False, "Grades must be numbers!"

    def delete_student(self, student_id):
        self.db.delete_student(student_id)
        return "Student deleted successfully!"

    def get_all_students(self):
        return self.db.fetch_all_students()
