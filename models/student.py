class Student:
    def __init__(self, student_id, name, lastname, grade1, grade2):
        self.student_id=student_id
        self.name=name
        self.lastname=lastname
        self.grade1=grade1
        self.grade2=grade2
        self.average=(grade1+ grade2)/ 2 if grade1 is not None and grade2 is not None else None


        
        