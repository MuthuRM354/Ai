def get_student_data():
    student = {}

    while True:
        try:
            count = int(input("Enter the number of students: "))
            if count <= 0:
                print("Please enter a number greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")


    for i in range(1, count + 1):
        name = input(f"Enter the name of student {i}: ").strip()

        while True:
            try:
                mark = int(input(f"Enter the marks for {name}: "))
                if mark < 0 or mark > 100:
                    print("Please enter a mark between 0 and 100.")
                    continue
                student[name] = mark
                break
            except ValueError:
                print("Invalid marks. Please enter a valid number.")

    return student

def save_to_file(student, filename="students_data.txt"):
    with open(filename, "w") as f:
     for name, mark in student.items():
        f.write(f"{name}: {mark}\n")
        print(f"{name}: {mark}")

def read_from_file(filename="students_data.txt"):
    student = {}
    with open(filename, "r") as f:
        for line in f:
            name, mark = line.strip().split(": ")
            student[name] = int(mark)
    return student

def print_report(student):
        print("Student Report:")
        print("--------------")
        print("Name\tMarks\tGrade\tStatus")
        print("--------------")
        
        for name, mark in student.items():
            if mark >= 90:
                grade = "A"
            elif mark >= 80:
                grade = "B"
            elif mark >= 70:
                grade = "C"
            elif mark >= 60:
                grade = "D"
            elif mark >= 45:
                grade = "E"
            else:
                grade = "F"

            status = "Pass" if mark >= 45 else "Fail"
            print(f"{name}\t{mark}\t{grade}\t{status}")
        

        print("--------------")
        print("Total Marks: ", sum(student.values()))
        print("Number of Students: ", len(student))
        print("--------------")
        average_marks = sum(student.values()) / len(student)
        print("Average Marks: ", f"{average_marks:.2f}")
        highest_mark = max(student, key=student.get)
        lowest_mark = min(student, key=student.get)
        print("--------------")
        print(f"Highest scorer:  {highest_mark}({student[highest_mark]})")
        print(f"Lowest scorer:  {lowest_mark}({student[lowest_mark]})")