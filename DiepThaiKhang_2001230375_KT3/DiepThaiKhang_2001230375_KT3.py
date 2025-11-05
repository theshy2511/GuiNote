import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import datetime
import re

FILE_NAME = "students.json"

def load_students():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            json.dump([], f)
        return []
    with open(FILE_NAME, 'r') as f:
        return json.load(f)

def save_students(students):
    with open(FILE_NAME, 'w') as f:
        json.dump(students, f, indent=4)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def generate_mssv():
    part1 = "2"
    part2 = f"{random.randint(1, 33):03d}"
    year_suffix = str(datetime.datetime.now().year)[-3:]
    part4 = f"{random.randint(0, 999):03d}"
    return part1 + part2 + year_suffix + part4

def add_student():
    tensv = entry_name.get().strip()
    email = entry_email.get().strip()

    if not tensv or not email:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Lỗi", "Email không hợp lệ.")
        return

    mssv = generate_mssv()
    new_student = {"mssv": mssv, "tensv": tensv, "email": email}
    students.append(new_student)
    save_students(students)
    refresh_student_list()
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def delete_student(index):
    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?"):
        del students[index]
        save_students(students)
        refresh_student_list()

def refresh_student_list():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    for index, s in enumerate(students):
        frame_item = tk.Frame(scrollable_frame)
        frame_item.grid(row=index, column=0, sticky="w", pady=2)

        info = f"{s['mssv']} - {s['tensv']} - {s['email']}"
        label = tk.Label(frame_item, text=info, anchor="w", width=60)
        label.pack(side="left")

        btn = tk.Button(frame_item, text="Delete", command=lambda i=index: delete_student(i))
        btn.pack(side="right", padx=10)

def search_students():
    keyword = entry_search.get().strip().lower()
    listbox_search.delete(0, tk.END)
    found = False
    for s in students:
        if keyword in s['tensv'].lower() or keyword in s['email'].lower():
            listbox_search.insert(tk.END, f"{s['mssv']} - {s['tensv']} - {s['email']}")
            found = True
    if not found:
        listbox_search.insert(tk.END, "Không tìm thấy sinh viên nào.")

root = tk.Tk()
root.title("Quản lý Sinh viên")
root.geometry("540x660")

main_frame = tk.Frame(root, padx=20, pady=10)
main_frame.pack(fill='both', expand=True)

frame_input = tk.Frame(main_frame, width=500)
frame_input.pack(pady=10, anchor='center')

tk.Label(frame_input, text="Tên sinh viên:", width=15, anchor='e').grid(row=0, column=0, sticky="e", pady=2)
entry_name = tk.Entry(frame_input, width=40)
entry_name.grid(row=0, column=1, pady=2, padx=5)

tk.Label(frame_input, text="Email sinh viên:", width=15, anchor='e').grid(row=1, column=0, sticky="e", pady=2)
entry_email = tk.Entry(frame_input, width=40)
entry_email.grid(row=1, column=1, pady=2, padx=5)

btn_add = tk.Button(frame_input, text="Thêm sinh viên", width=15, command=add_student)
btn_add.grid(row=2, column=0, columnspan=2, pady=10)

frame_list_outer = tk.Frame(main_frame)
frame_list_outer.pack(fill='both', expand=True, pady=5)

tk.Label(frame_list_outer, text="Danh sách sinh viên:", anchor="w").pack(anchor="w")

frame_list_container = tk.Frame(frame_list_outer)
frame_list_container.pack(fill='both', expand=True)

canvas = tk.Canvas(frame_list_container, height=200)
scrollbar = tk.Scrollbar(frame_list_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_search = tk.Frame(main_frame)
frame_search.pack(fill='x', pady=15)

tk.Label(frame_search, text="Tìm kiếm sinh viên:", width=15, anchor='w').grid(row=0, column=0, sticky="w", pady=2)
entry_search = tk.Entry(frame_search, width=40)
entry_search.grid(row=0, column=1, pady=2, padx=5)

tk.Button(frame_search, text="Tìm kiếm", command=search_students).grid(row=0, column=2, padx=5)

tk.Label(main_frame, text="Kết quả tìm kiếm:").pack(anchor="w", pady=(0, 5))
listbox_search = tk.Listbox(main_frame, width=70)
listbox_search.pack(fill='x')

students = load_students()
refresh_student_list()

root.mainloop()
