import matplotlib.pyplot as plt

def display_comparison_chart(students):
    names = [f"{student[1]} {student[2]}" for student in students]
    grades1 = [student[3] for student in students]
    grades2 = [student[4] for student in students]

    x = range(len(names))
    plt.figure(figsize=(8, 5))
    plt.bar(x, grades1, width=0.4, label="Grade 1")
    plt.bar([p + 0.4 for p in x], grades2, width=0.4, label="Grade 2")
    plt.xticks([p + 0.2 for p in x], names, rotation=30)
    plt.xlabel("Students")
    plt.ylabel("Grades")
    plt.title("Comparison of Students")
    plt.legend()
    plt.tight_layout()
    plt.show()
