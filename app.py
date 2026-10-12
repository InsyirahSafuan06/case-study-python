import streamlit as st
import numpy as np
import pandas as pd

# Import class dan function dari analysis.py
from analysis import Student
from analysis import calculate_subject_avg
from analysis import calculate_subject_median
from analysis import calculate_subject_std

# Tajuk sistem
st.title("Student Performance Analysis System")
st.write("Analyse student marks and academic performance.")

# Senarai subjek yang digunakan
subjects = ["Python Programming", "Full Stack Development", "Object-Oriented Programming"]

# Simpan data semua pelajar
if "students" not in st.session_state:
    st.session_state.students = []

# Bahagian untuk masukkan maklumat pelajar
st.header("Student Information")

# Semua input diletakkan dalam satu form
with st.form("student_form"):

    # Masukkan nama dan ID pelajar
    name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    # Masukkan markah untuk setiap subjek
    python_mark = st.text_input("Python Programming Marks")
    full_stack_mark = st.text_input("Full Stack Development Marks")
    oop_mark = st.text_input("Object-Oriented Programming Marks")

    # Button untuk hantar maklumat
    submit = st.form_submit_button("Analyse Student")

# Proses data bila button ditekan
if submit:
    try:
        # Check kalau nama atau ID tak diisi
        if name == "" or student_id == "":
            st.error("Please enter student name and ID.")

        # Check kalau ada markah yang kosong
        elif (python_mark == "" or full_stack_mark == ""
              or oop_mark == ""):
            st.error("Please enter all subject marks.")

        else:
            # Tukar markah kepada nombor
            mark1 = float(python_mark)
            mark2 = float(full_stack_mark)
            mark3 = float(oop_mark)

            # Simpan semua markah dalam satu list
            marks = [mark1, mark2, mark3]

            # Check kalau markah kurang 0 atau lebih 100
            if any(mark < 0 or mark > 100 for mark in marks):
                st.error("Marks must be between 0 and 100.")

            else:
                # Check kalau ID pelajar dah ada dalam list
                duplicate = False

                for student in st.session_state.students:
                    if student.id == student_id:
                        duplicate = True
                        break

                # Papar error kalau ID sama
                if duplicate:
                    st.error("Student ID already exists.")

                else:
                    # Simpan maklumat pelajar sebagai objek
                    student = Student(name, student_id, marks)

                    # Masukkan pelajar dalam list
                    st.session_state.students.append(student)

                    # Papar mesej bila data dah disimpan
                    st.success("Student information saved.")

    # Papar error kalau markah yang dimasukkan bukan nombor
    except ValueError:
        st.error("Please enter valid numbers for all marks.")

# Papar result kalau dah ada data pelajar
if len(st.session_state.students) > 0:

    st.header("Student Results")

    # Kumpulkan result semua pelajar
    report = []

    # Ambil data setiap pelajar
    for student in st.session_state.students:

        # Kira jumlah markah pelajar
        total = np.sum(student.marks)

        # Simpan maklumat dan result dalam list
        report.append({
            "Student ID": student.id,
            "Student Name": student.name,
            "Python Programming": student.marks[0],
            "Full Stack Development": student.marks[1],
            "Object-Oriented Programming": student.marks[2],
            "Total": total,
            "Average": round(student.get_average(), 2),
            "Highest": student.get_highest(),
            "Lowest": student.get_lowest(),
            "Grade": student.determine_grade()
        })

    # Tukar result kepada jadual
    report_df = pd.DataFrame(report)

    # Papar result semua pelajar
    st.dataframe(report_df, use_container_width=True)

    # Ringkasan result semua pelajar
    st.subheader("Overall Summary")

    # Bahagikan paparan kepada tiga bahagian
    col1, col2, col3 = st.columns(3)

    # Papar jumlah pelajar
    col1.metric(
        "Total Students",
        len(st.session_state.students)
    )

    # Kira purata markah semua pelajar
    col2.metric(
        "Average Marks",
        round(report_df["Average"].mean(), 2)
    )

    # Papar jumlah markah paling tinggi
    col3.metric(
        "Highest Total",
        int(report_df["Total"].max())
    )

    # Gabungkan markah pelajar dalam NumPy matrix
    marks_matrix = np.array([
        student.marks for student in st.session_state.students
    ])

    # Papar matrix markah
    st.header("Matrix Analysis")
    st.write("Marks Matrix:")
    st.write(marks_matrix)

    # Kira jumlah markah setiap pelajar
    total_marks = np.sum(marks_matrix, axis=1)

    # Kira purata markah setiap pelajar
    average_marks = np.mean(marks_matrix, axis=1)

    # Papar summary berdasarkan matrix
    st.subheader("Student Matrix Summary")

    # Buat jadual untuk jumlah dan purata markah
    matrix_report = pd.DataFrame({
        "Student Name": [
            student.name for student in st.session_state.students
        ],
        "Total Marks": total_marks,
        "Average Marks": np.round(average_marks, 2)
    })

    # Papar jadual matrix
    st.dataframe(matrix_report, use_container_width=True)

    # Cari pelajar yang dapat jumlah markah paling tinggi
    top_index = np.argmax(total_marks)

    # Papar nama pelajar tersebut
    st.write(
        "Top Performing Student:",
        st.session_state.students[top_index].name
    )

    # Papar jumlah markah tertinggi
    st.write("Highest Total Marks:", int(total_marks[top_index]))

    # Analisis markah untuk setiap subjek
    st.header("Subject Statistical Analysis")

    # Buat analisis untuk semua subjek
    for i in range(len(subjects)):

        # Ambil markah semua pelajar untuk subjek ni
        subject_marks = marks_matrix[:, i]

        # Kira mean, median dan standard deviation
        average = calculate_subject_avg(subject_marks)
        median = calculate_subject_median(subject_marks)
        standard_deviation = calculate_subject_std(subject_marks)

        # Papar nama subjek
        st.subheader(subjects[i])

        # Bahagikan result kepada tiga bahagian
        col1, col2, col3 = st.columns(3)

        # Papar result analisis
        col1.metric("Mean", round(average, 2))
        col2.metric("Median", round(median, 2))
        col3.metric(
            "Standard Deviation",
            round(standard_deviation, 2)
        )

# Papar mesej ni kalau belum ada data pelajar
else:
    st.info("Enter student information to view the analysis.")