from models.database import StudentDatabase

class StudentController:
    def __init__(self):
        self.db=StudentDatabase()


    def add_student(self, student):
        self.db.save_student(student)

    
    def get_students(self):
        return self.db.fetch_all_students()
        