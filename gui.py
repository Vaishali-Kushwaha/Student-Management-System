import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import mysql.connector

# =========================
# MySQL Connection
# =========================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="diva@2507",
    database="student_management"
)

cursor = db.cursor()

def clear_form():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)

# =========================
# Add Student
# =========================

def add_student():

    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    branch = branch_entry.get()
    semester = semester_entry.get()

    # Name and Email validation
    if not name or not email:
        messagebox.showwarning(
            "Required",
            "Name and Email are required."
        )
        return

    # Email validation
    if "@" not in email or "." not in email:
        messagebox.showwarning(
            "Invalid Email",
            "Please enter a valid email address."
        )
        return

    # Phone validation
    if phone and (not phone.isdigit() or len(phone) != 10):
        messagebox.showwarning(
            "Invalid Phone",
            "Phone number must contain exactly 10 digits."
        )
        return

    # Age validation
    if age and (not age.isdigit() or int(age) <= 0):
        messagebox.showwarning(
            "Invalid Age",
            "Age must be a valid positive number."
        )
        return

    # Course validation
    if course == "":
        messagebox.showwarning(
            "Invalid Course",
            "Please enter your course."
        )
        return

    # Branch validation
    if branch == "":
        messagebox.showwarning(
            "Invalid Branch",
            "Please enter your branch."
        )
        return

    # Semester validation
    if semester and (not semester.isdigit() or not 1 <= int(semester) <= 8):
        messagebox.showwarning(
            "Invalid Semester",
            "Semester must be between 1 and 8."
        )
        return

    cursor.execute("SELECT id from students WHERE email = %s", (email,))
    existing_student=cursor.fetchone()
    if existing_student:
        messagebox.showwarning("Duplicate Email","This email is already registered!")
        return

    # Insert data
    query = """
        INSERT INTO students
        (name, email, phone, age, course, branch, semester)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        name,
        email,
        phone,
        age,
        course,
        branch,
        semester
    )

    cursor.execute(query, values)
    db.commit()

    messagebox.showinfo(
        "Success",
        "Student added successfully!"
    )

    # Clear fields
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    semester_entry.delete(0, tk.END)


# =========================
# View Students
# =========================

def view_students():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    student_window = tk.Toplevel(root)
    student_window.title("All Students")
    student_window.geometry("1100x400")

    table_container = tk.Frame(student_window)
    table_container.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

    table_frame = tk.Frame(table_container)
    table_frame.pack(
    side="left",
    fill="both",
    expand=True
)

    scrollbar = tk.Scrollbar(
    table_container,
    orient="vertical"
)
    scrollbar.pack(
    side="right",
    fill="y"
)

    headings = [
        "ID",
        "Name",
        "Email",
        "Phone",
        "Age",
        "Course",
        "Branch",
        "Semester"
    ]

    for col, heading in enumerate(headings):
        tk.Label(
            table_frame,
            text=heading,
            font=("Arial", 11, "bold"),
            bg="teal",
            fg="white",
            borderwidth=1,
            relief="solid",
            width=15
        ).grid(row=0, column=col, sticky="nsew")

    for row, student in enumerate(students, start=1):
        for col, value in enumerate(student):
            tk.Label(
                table_frame,
                text=str(value),
                font=("Arial", 10),
                borderwidth=1,
                relief="solid",
                width=15
            ).grid(row=row, column=col, sticky="nsew")

    for col in range(8):
        table_frame.grid_columnconfigure(
            col,
            weight=1
        )


# =========================
# Delete Student
# =========================

def delete_student():

    student_id = simpledialog.askinteger(
        "Delete Student",
        "Enter Student ID to delete:"
    )

    if student_id:
        confirm=messagebox.askyesno("Confirm Delete","Are you sure you want to delete this student?")
        if not confirm:
            return
        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success",
                "Student deleted successfully!"
            )
        else:
            messagebox.showwarning(
                "Not Found",
                "Student ID not found!"
            )


# =========================
# Update Student
# =========================

def update_student():
    student_id = simpledialog.askinteger(
        "Update Student",
        "Enter Student ID:"
    )

    if not student_id:
        return

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        messagebox.showwarning(
            "Not Found",
            "Student ID not found!"
        )
        return

    update_window = tk.Toplevel(root)
    update_window.title("Update Student")
    update_window.geometry("450x500")

    tk.Label(
        update_window,
        text="Update Student Details",
        font=("Arial", 18, "bold"),
        fg="darkblue"
    ).pack(pady=15)

    tk.Label(update_window, text="Name",
             font=("Arial", 10, "bold")).pack()
    new_name_entry = tk.Entry(update_window, width=35)
    new_name_entry.pack(pady=5)
    new_name_entry.insert(0, student[1])

    tk.Label(update_window, text="Email",
             font=("Arial", 10, "bold")).pack()
    new_email_entry = tk.Entry(update_window, width=35)
    new_email_entry.pack(pady=5)
    new_email_entry.insert(0, student[2])

    tk.Label(update_window, text="Phone",
             font=("Arial", 10, "bold")).pack()
    new_phone_entry = tk.Entry(update_window, width=35)
    new_phone_entry.pack(pady=5)
    new_phone_entry.insert(0, student[3])

    tk.Label(update_window, text="Age",font=("Arial",10,"bold")).pack()
    new_age_entry=tk.Entry(update_window, width=35)
    new_age_entry.pack(pady=5)
    new_age_entry.insert(0, student[4])

    tk.Label(update_window, text="Course",
             font=("Arial", 10, "bold")).pack()
    new_course_entry = tk.Entry(update_window, width=35)
    new_course_entry.pack(pady=5)
    new_course_entry.insert(0, student[5])

    tk.Label(update_window, text="Branch",
                 font=("Arial", 10, "bold")).pack()
    new_branch_entry = tk.Entry(update_window, width=35)
    new_branch_entry.pack(pady=5)
    new_branch_entry.insert(0, student[6])

    tk.Label(update_window, text="Semester",
                 font=("Arial", 10, "bold")).pack()
    new_semester_entry = tk.Entry(update_window, width=35)
    new_semester_entry.pack(pady=5)
    new_semester_entry.insert(0, student[7])
    
    

    def save_update():
        new_name = new_name_entry.get()
        new_email = new_email_entry.get()
        new_phone = new_phone_entry.get()
        new_age = new_age_entry.get()
        new_course = new_course_entry.get()
        new_branch = new_branch_entry.get()
        new_semester = new_semester_entry.get()

        if not new_name or not new_email:
            messagebox.showwarning(
                "Required",
                "Name and Email are required."
            )
            return

        if "@" not in new_email or "." not in new_email:
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return

        if new_phone and (
            not new_phone.isdigit()
            or len(new_phone) != 10
        ):
            messagebox.showwarning(
                "Invalid Phone",
                "Phone number must contain exactly 10 digits."
            )
            return

        if new_age and (not new_age.isdigit() or int(new_age) <= 0):
            messagebox.showwarning("Invalid Age","Age must be a valid positive number.")
            return

        if new_branch == "":
            messagebox.showwarning("Invalid Branch","Please enter your branch.")
            return

        if new_semester and (
            not new_semester.isdigit()
            or not 1 <= int(new_semester) <= 8):
            messagebox.showwarning("Invalid Semester","Semester must be between 1 and 8.")
            return

        cursor.execute(
            """
            UPDATE students
            SET name = %s,
                email = %s,
                phone = %s,
                age = %s,
                course = %s,
                branch = %s,
                semester = %s
            WHERE id = %s
            """,
            (
                new_name,
                new_email,
                new_phone,
                new_age,
                new_course,
                new_branch,
                new_semester,
                student_id
            )
        )

        db.commit()

        messagebox.showinfo(
            "Success",
            "Student details updated successfully!"
        )

        update_window.destroy()

    update_button = tk.Button(
        update_window,
        text="Save Changes",
        command=save_update,
        width=20,
        font=("Arial", 10, "bold"),
        bg="teal",
        fg="white"
    )
    update_button.pack(pady=20)

        

    


# =========================
# Search Student
# =========================

def search_student():
    search_value = simpledialog.askstring(
        "Search Student",
        "Enter Student ID or Name:"
    )

    if not search_value:
        return

    if search_value.isdigit():
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (int(search_value),)
        )
    else:
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s",
            (f"%{search_value}%",)
        )

    students = cursor.fetchall()

    if not students:
        messagebox.showwarning(
            "Not Found",
            "No student found!"
        )
        return

    search_window = tk.Toplevel(root)
    search_window.title("Search Results")
    search_window.geometry("1100x300")

    table_frame = tk.Frame(search_window)
    table_frame.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    headings = [
        "ID", "Name", "Email", "Phone",
        "Age", "Course", "Branch", "Semester"
    ]

    for col, heading in enumerate(headings):
        tk.Label(
            table_frame,
            text=heading,
            font=("Arial", 11, "bold"),
            borderwidth=1,
            relief="solid",
            width=15
        ).grid(row=0, column=col, sticky="nsew")

    for row, student in enumerate(students, start=1):
        for col, value in enumerate(student):
            tk.Label(
                table_frame,
                text=str(value),
                font=("Arial", 10),
                borderwidth=1,
                relief="solid",
                width=15
            ).grid(row=row, column=col, sticky="nsew")

    for col in range(8):
        table_frame.grid_columnconfigure(
            col,
            weight=1
        )


# =========================
# Main Window
# =========================

root = tk.Tk()

root.title("Student Management System")
root.geometry("600x650")
root.configure(bg="aliceblue")


heading = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 22, "bold"),
    fg="darkblue", bg="aliceblue"
)
heading.pack(pady=20)


# Name
tk.Label(root, text="Name",font=("Arial",10,"bold"), bg="aliceblue").pack()
name_entry = tk.Entry(root, width=40,font=("Arial",10))
name_entry.pack(pady=4)


# Email
tk.Label(root, text="Email",font=("Arial",10,"bold"), bg="aliceblue").pack()
email_entry = tk.Entry(root, width=40,font=("Arial",10))
email_entry.pack(pady=4)


# Phone
tk.Label(root, text="Phone",font=("Arial",10,"bold"), bg="aliceblue").pack()
phone_entry = tk.Entry(root, width=40,font=("Arial",10))
phone_entry.pack(pady=4)


# Age
tk.Label(root, text="Age",font=("Arial",10,"bold"), bg="aliceblue").pack()
age_entry = tk.Entry(root, width=40,font=("Arial",10))
age_entry.pack(pady=4)


# Course
tk.Label(root, text="Course",font=("Arial",10,"bold"), bg="aliceblue").pack()
course_entry = ttk.Combobox(
    root,
    values = ["B.Tech","BCA","B.Sc","M.Tech"],
    width = 40,
    font = ("Arial",10)
)
course_entry.pack(pady=5)


# Branch
tk.Label(root, text="Branch",font=("Arial",10,"bold"), bg="aliceblue").pack()
branch_entry = ttk.Combobox(
    root,
    values = ["CSE","IT","ECE","EEE","Mechanical","Civil"],
    width = 40,
    font = ("Arial",10)
)
branch_entry.pack(pady=5)


# Semester
tk.Label(root, text="Semester",font=("Arial",10,"bold"), bg="aliceblue").pack()
semester_entry = ttk.Combobox(
    root,
    values = ["1","2","3","4","5","6","7","8"],
    width = 40,
    font = ("Arial",10),
    state = "readonly"
)
semester_entry.pack(pady=5)


# Buttons
button_frame = tk.Frame(root,bg="aliceblue")
button_frame.pack(pady=15)

#add button
add_button = tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    width=20,
    font=("Arial",10,"bold"),
    bg="teal",
    fg="white"
)
add_button.pack(pady=8)

add_button.bind(
    "<Enter>",
            lambda event:
            add_button.config(bg="#006666")
)
add_button.bind(
    "<Leave>",
    lambda event:
    add_button.config(bg="teal")
)

#view button
view_button = tk.Button(
    button_frame,
    text="View Students",
    command=view_students,
    width=20,
    font=("Arial",10,"bold"),
    bg="teal",
    fg="white"
)
view_button.pack(pady=8)

view_button.bind(
    "<Enter>",
            lambda event:
            view_button.config(bg="#006666")
)
view_button.bind(
    "<Leave>",
    lambda event:
    view_button.config(bg="teal")
)

#search button
search_button = tk.Button(
    button_frame,
    text="Search Student",
    command=search_student,
    width=20,
    font=("Arial",10,"bold"),
    bg="teal",
    fg="white"
)
search_button.pack(pady=8)

search_button.bind(
    "<Enter>",
            lambda event:
            search_button.config(bg="#006666")
)
search_button.bind(
    "<Leave>",
    lambda event:
    search_button.config(bg="teal")
)

#update button
update_button = tk.Button(
    button_frame,
    text="Update Student",
    command=update_student,
    width=20,
    font=("Arial",10,"bold"),
    bg="teal",
    fg="white"
)
update_button.pack(pady=8)

update_button.bind(
    "<Enter>",
            lambda event:
            update_button.config(bg="#006666")
)
update_button.bind(
    "<Leave>",
    lambda event:
    update_button.config(bg="teal")
)

#delete button
delete_button = tk.Button(
    button_frame,
    text="Delete Student",
    command=delete_student,
    width=20,
    font=("Arial",10,"bold"),
    bg="teal",
    fg="white"
)
delete_button.pack(pady=8)

delete_button.bind(
    "<Enter>",
            lambda event:
            delete_button.config(bg="#006666")
)
delete_button.bind(
    "<Leave>",
    lambda event:
    delete_button.config(bg="teal")
)

#clear button
clear_button = tk.Button(
    button_frame,
    text="Clear Form",
    command=clear_form,
    width=20,
    font=("Arial",10,"bold"),
    bg="teal",
    fg="white"
)
clear_button.pack(pady=8)

clear_button.bind(
    "<Enter>",
            lambda event:
            clear_button.config(bg="#006666")
)
clear_button.bind(
    "<Leave>",
    lambda event:
    clear_button.config(bg="teal")
)

#exit function
def exit_app():
    confirm=messagebox.askyesno("Exit","Are you sure you want  to exit?")
    if confirm:
        cursor.close()
        db.close()
        root.destroy()

#exit button
exit_button=tk.Button(
    button_frame,
    text="Exit",
    command=exit_app,
    width=20,
    font=("Arial",10,"bold"),
    bg="teal",
    fg="white"
)
exit_button.pack(pady=8)

exit_button.bind(
    "<Enter>",
            lambda event:
            exit_button.config(bg="#006666")
)
exit_button.bind(
    "<Leave>",
    lambda event:
    exit_button.config(bg="teal")
)

root.mainloop()