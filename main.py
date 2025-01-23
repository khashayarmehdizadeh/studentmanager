from controllers.student_controller import StudentController
from views.student_view import StudentView

if __name__ == "__main__":
    controller = StudentController()
    view = StudentView(controller)
    view.run()
