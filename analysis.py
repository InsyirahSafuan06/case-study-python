import streamlit as st
import numpy as np
import pandas as pd

# Import class dan function dari analysis.py
from analysis import (Student,calculate_subject_avg,calculate_subject_median,calculate_subject_std)

# Tajuk sistem
st.title("Student Performance Analysis System")
st.write("Analyse student marks and academic performance.")

# Senarai subjek yang digunakan
subjects = ["Python Programming", "Full Stack Development", "Object-Oriented Programming"]

# Simpan data semua pelajar
if "students" not in st.session_state:
    st.session_state.students = []

st.header("Student Information") # Bahagian untuk masukkan maklumat pelajar

# Semua input dalam satu form
with st.form("student_form"):

    # Masukkan nama dan ID pelajar
    name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    # Masukkan markah untuk setiap subjek
    python_mark = st.text_input("Python Programming Marks")
    full_stack_mark = st.text_input("Full Stack Development Marks")
    oop_mark = st.text_input("Object-Oriented Programming Marks")

    submit = st.form_submit_button("Analyse Student")


# Proses data bila button ditekan
if submit:
    try:
        # Check kalau nama atau ID tak diisi
        if name == "" or student_id == "":
            st.error("Please enter student name and ID.")

        else:
            # Tukar markah kepada integer
            python_mark = int(python_mark)
            full_stack_mark = int(full_stack_mark)
            oop_mark = int(oop_mark)

            marks = [python_mark, full_stack_mark, oop_mark]

            # Check kalau markah di luar julat
            if any(mark < 0 or mark > 100 for mark in marks):
                st.error("Marks must be between 0 and 100.")

            else:
                duplicate = False

                # Check kalau ID pelajar dah ada
                for student in st.session_state.students:
                    if student.id == student_id:
                        duplicate = True
                        break

                # Papar error kalau ID sama
                if duplicate:
                    st.error("Student ID already exists.")

                else:
                    student = Student(name, student_id, marks)
                    st.session_state.students.append(student)

                    st.success("Student information saved.")

    except (ValueError, TypeError):
        st.error("Please enter valid student information.")
        
# Papar result kalau dah ada data pelajar
if len(st.session_state.students) > 0:
    st.header("Student Results")

    report = []  # Kumpulkan result semua pelajar

    for student in st.session_state.students:  # Ambil data setiap pelajar

        total = np.sum(student.marks) # Kira jumlah markah pelajar

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

    report_df = pd.DataFrame(report) # Tukar result kepada jadual

    # Papar result semua pelajar
    st.dataframe(report_df, use_container_width=True)

    st.subheader("Overall Summary") # Ringkasan result semua pelajar

    col1, col2, col3 = st.columns(3) # Bahagikan paparan kepada tiga bahagian

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

    total_marks = np.sum(marks_matrix, axis=1) # Kira jumlah markah setiap pelajar
    average_marks = np.mean(marks_matrix, axis=1) # Kira purata markah setiap pelajar

    st.subheader("Student Matrix Summary") # Papar summary berdasarkan matrix

    # Buat jadual untuk jumlah dan purata markah
    matrix_report = pd.DataFrame({
        "Student Name": [
            student.name for student in st.session_state.students
        ],
        "Total Marks": total_marks,
        "Average Marks": np.round(average_marks, 2)
    })

    st.dataframe(matrix_report, use_container_width=True) # Papar jadual matrix

    top_index = np.argmax(total_marks)  # Cari pelajar yang dapat jumlah markah paling tinggi

    # Papar nama pelajar tersebut
    st.write(
        "Top Performing Student:",
        st.session_state.students[top_index].name
    )

    st.write("Highest Total Marks:", int(total_marks[top_index])) # Papar jumlah markah tertinggi

    st.header("Subject Statistical Analysis") # Analisis markah untuk setiap subjek

    # Buat analisis untuk semua subjek
    for i in range(len(subjects)):

        subject_marks = marks_matrix[:, i] # Ambil markah semua pelajar untuk subjek

        # Kira mean, median dan standard deviation
        average = calculate_subject_avg(subject_marks)
        median = calculate_subject_median(subject_marks)
        standard_deviation = calculate_subject_std(subject_marks)

        st.subheader(subjects[i]) # Papar nama subjek

        col1, col2, col3 = st.columns(3) # Bahagikan result kepada tiga bahagian

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