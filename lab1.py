import mysql.connector

# Підключення до бази даних
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="lab1"
)

# Створення курсора для виконання запитів
cursor = db.cursor()

# 2. Створення таблиці students
cursor.execute("""
    CREATE TABLE students (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        age INT,
        email VARCHAR(255)
    )
""")

# 3. Додавання 5 студентів до таблиці students
students_data = [
    ("John Doe", 20, "john.doe@example.com"),
    ("Jane Smith", 22, "jane.smith@example.com"),
    ("Michael Johnson", 19, "michael.johnson@example.com"),
    ("Emily Davis", 21, "emily.davis@example.com"),
    ("Daniel Wilson", 20, "daniel.wilson@example.com")
]

cursor.executemany("INSERT INTO students (name, age, email) VALUES (%s, %s, %s)", students_data)

# 4. Вибірка всіх студентів з таблиці students
cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()
print("All students:")
for student in all_students:
    print(student)

# 5. Вибірка студента з таблиці students за ім'ям
name = "John Doe"
cursor.execute("SELECT * FROM students WHERE name = %s", (name,))
student_by_name = cursor.fetchone()
print(f"Student by name '{name}':")
print(student_by_name)

# 6. Оновлення віку одного зі студентів в таблиці students
student_id = 1
new_age = 21
cursor.execute("UPDATE students SET age = %s WHERE id = %s", (new_age, student_id))
db.commit()

# 7. Видалення студента з таблиці students за заданим ідентифікатором
student_id = 3
cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
db.commit()

# 8. Використання транзакцій для додавання ще двох студентів до таблиці students
try:
    cursor.execute("START TRANSACTION")

    new_students_data = [
        ("Sarah Johnson", 22, "sarah.johnson@example.com"),
        ("Robert Davis", 20, "robert.davis@example.com")
    ]

    cursor.executemany("INSERT INTO students (name, age, email) VALUES (%s, %s, %s)", new_students_data)

    db.commit()
except mysql.connector.Error as error:
    print("Transaction rolled back:", error)
    db.rollback()

# 9. Створення таблиці courses
cursor.execute("""
    CREATE TABLE courses (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        description VARCHAR(255),
        credits INT
    )
""")

# 10. Додавання 3 курсів до таблиці courses
courses_data = [
    ("Mathematics", "Introduction to mathematics", 3),
    ("Computer Science", "Introduction to computer science", 4),
    ("English Literature", "Introduction to English literature", 3)
]

cursor.executemany("INSERT INTO courses (name, description, credits) VALUES (%s, %s, %s)", courses_data)

# 11. Створення таблиці student_courses
cursor.execute("""
    CREATE TABLE student_courses (
        student_id INT,
        course_id INT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
""")

# 12. Заповнення таблиці student_courses даними про курси, які вибрали студенти
student_courses_data = [
    (1, 1),  # John Doe - Mathematics
    (1, 2),  # John Doe - Computer Science
    (2, 1),  # Jane Smith - Mathematics
    (3, 3)   # Michael Johnson - English Literature
]

cursor.executemany("INSERT INTO student_courses (student_id, course_id) VALUES (%s, %s)", student_courses_data)

# 13. Вибірка всіх студентів, які вибрали певний курс
course_id = 1
cursor.execute("""
    SELECT students.*
    FROM students
    INNER JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.course_id = %s
""", (course_id,))
students_for_course = cursor.fetchall()
print(f"All students for course with ID {course_id}:")
for student in students_for_course:
    print(student)

# 14. Вибірка всіх курсів, які вибрали студенти за певним ім'ям
student_name = "John Doe"
cursor.execute("""
    SELECT courses.*
    FROM courses
    INNER JOIN student_courses ON courses.id = student_courses.course_id
    INNER JOIN students ON students.id = student_courses.student_id
    WHERE students.name = %s
""", (student_name,))
courses_for_student = cursor.fetchall()
print(f"All courses for student '{student_name}':")
for course in courses_for_student:
    print(course)

# 15. Вибірка всіх студентів та їх курсів, використовуючи JOIN
cursor.execute("""
    SELECT students.*, courses.*
    FROM students
    INNER JOIN student_courses ON students.id = student_courses.student_id
    INNER JOIN courses ON courses.id = student_courses.course_id
""")
students_with_courses = cursor.fetchall()
print("All students and their courses:")
for row in students_with_courses:
    student_id, student_name, student_age, student_email, course_id, course_name, course_description, course_credits = row
    print(f"Student: {student_name} (ID: {student_id})")
    print(f"Course: {course_name} (ID: {course_id})")
    print("---")

# Закриття курсора та з'єднання з базою даних
cursor.close()
db.close()
