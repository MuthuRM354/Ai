# from src.students import get_student_data, save_to_file, read_from_file, print_report

# name = input("What is your name? ")
# age = int(input("How old are you? "))
# print("Hello, " + name + "! You are " + str(age) + " years old. Welcome to the world of programming!")
# print("Next year your age will be ", age + 1, ".")

# if age < 18:
#     print("You are a minor. Enjoy your youth!")
# elif age < 65:
#     print("You are an adult. Keep working hard!")
# else:
#     print("You are a senior. Enjoy your retirement!")

# number = int(input("Enter a number: "))
# if number >0:
#     print("The number is positive.")
# elif number < 0:
#     print("The number is negative.")
# else:    
#     print("The number is zero.")

# for i in range(1, 6):
#     print("count ", i)

# number = int(input("Enter a number to get their multiplication table: "))

# print("Multiplication table for ", number)
# for i in range(1, 11):
#     print(number, " x ", i, " = ", number * i) 


# secret_number = 7
# while True:
#     number = int(input("Enter a number to check if it is correct guess: "))
#     if number == secret_number:
#         print("Congratulations! You guessed the correct number.")
#         break
#     else:
#         print("Wrong guess. Try again!")

# def odd_or_even(number):
#     if number % 2 == 0:
#         return "Even"
#     else:
#         return "Odd"
    
# number = int(input("Enter a number to check if it is odd or even: "))
# result = odd_or_even(number)
# print("The number ", number, " is ", result, ".")

# def calculator (a, b, op):
#     if op == '+':
#         return a + b
#     elif op =='-':
#         return a-b
#     elif op == '*':
#         return a * b
#     elif op == '/':
#         if b != 0:
#             return a / b
#         else:
#             return "Error: Division by zero is not allowed."
#     else:
#         return "Error: Invalid operator. Please use +, -, *, or /."
    
# num1 = float(input("Enter the first number: "))
# num2 = float(input("Enter the second number: "))
# operator = input("Enter the operator (+, -, *, /): ")
# result1 = calculator(num1, num2, operator)
# result2 = calculator(10, 3, '/')
# print("The result of the calculation is: ", f"{result1:.2f}")
# print("The result is: ", f"{result2:.2f}")

# marks = [85, 90, 78, 92, 88]

# def calculate_statistics(marks):
#     total_marks = sum(marks)
#     average_marks = total_marks / len(marks)
#     max_marks = max(marks)
#     min_marks = min(marks)
#     print("Total marks: ", total_marks)
#     print("Average marks: ", f"{average_marks:.2f}")
#     print("Maximum marks: ", max_marks)
#     print("Minimum marks: ", min_marks)

# calculate_statistics(marks)

# book = {
#     "title": "The Great Gatsby",
#     "author": "F. Scott Fitzgerald",
#     "year_published": 1925,
#     "price": 1399
# }

# def update_price(book, new_price):
#     book['price'] = new_price
# for key, value in book.items():
#     print(key + ": " + str(value)) 


# update_price(book, book["price"] + 50)
# # print("price is updated to ", f"{float(book['price'])}")
# print("The book is ", book['title'], " by ", book['author'], " published in ", book['year_published'], " with a price of ", book["price"], ".")

# from distro import name

# def create_students_file():
#     with open("students.txt", "w") as f:
#         f.write("Alice: 90\n")
#         f.write("Bob: 85\n")
#         f.write("Charlie: 92\n")

# def read_and_calculate():
#     with open("students.txt", "r") as f:
#         print("Student Marks:")
#         print("--------------")
#         print("Name\tMarks")
#         print("--------------")
#         marks = []
#         for line in f:
#             name, mark = line.strip().split(": ")
#             marks.append(int(mark))
#             print(f"{name}\t{mark}")
#         print("--------------")
#         print("Total Marks: ", sum(marks))
#         print("Number of Students: ", len(marks))
#         print("--------------")
#         average_marks = sum(marks) / len(marks)
#         print("Average Marks: ", f"{average_marks:.2f}")



# create_students_file()
# read_and_calculate()

# def main():
#     student_data = get_student_data()
#     save_to_file(student_data)
#     loaded_data = read_from_file()
#     print_report(loaded_data)

# main()

# from src.llm import get_llm

# def main():
#     try:
#         llm = get_llm()
#     except RuntimeError as err:
#         print(err)
#         return

#     question = input("Ask a Python question: ")
#     response = llm.invoke(question)
#     print("\nAnswer:\n", response.content)

# if __name__ == "__main__":
#     main()

from src.llm import get_llm

def main():
    try:
        llm = get_llm()
        question = input("Ask anything: ")
        response = llm.invoke(question)
        print("\nAnswer:\n", response.content)
    except Exception as e:
        print("Error:", e)

    save = input("Do you want to save the response to a file? (yes/no): ")
    if save.lower() == "yes":  
        filename = input("Enter the filename to save the response: ")
        try:
            with open(filename, "w") as f:
                f.write(response.content)
        except Exception as e:
            print("Error saving file:", e)

if __name__ == "__main__":
    main()