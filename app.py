import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="diva@2507",
    database="student_management"
)

cursor = connection.cursor()


# Add Student
def add_student():
    name = input("Enter student name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    age = int(input("Enter age: "))
    course = input("Enter course: ")
    branch = input("Enter branch: ")
    semester = int(input("Enter semester: "))

    query = """
    INSERT INTO students
    (name, email, phone, age, course, branch, semester)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (name, email, phone, age, course, branch, semester)

    cursor.execute(query, values)
    connection.commit()

    print("Student added successfully!")


# View Students
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n===== STUDENT LIST =====")

    if len(students) == 0:
        print("No students found.")
    else:
        for student in students:
            print(student)


# Update Student
def update_student():
    student_id = int(input("Enter student ID to update: "))

    new_email = input("Enter new email: ")
    new_phone = input("Enter new phone: ")

    query = """
    UPDATE students
    SET email = %s, phone = %s
    WHERE id = %s
    """

    values = (new_email, new_phone, student_id)

    cursor.execute(query, values)
    connection.commit()

    if cursor.rowcount > 0:
        print("Student updated successfully!")
    else:
        print("Student ID not found.")


# Delete Student
def delete_student():
    student_id = int(input("Enter student ID to delete: "))

    query = "DELETE FROM students WHERE id = %s"

    cursor.execute(query, (student_id,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student ID not found.")


# Main Menu
while True:

    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("Program closed.")
        break

    else:
        print("Invalid choice. Please try again.")


cursor.close()
connection.close()