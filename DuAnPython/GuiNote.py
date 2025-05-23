import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

USER_FILE = "users.json"
notes_data = []
NOTES_FILE = "notes.json"

#  --------------------- CĂN GIỮA MÀN HÌNH ---------------------
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# --------------------- XỬ LÝ DỮ LIỆU ---------------------
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def load_notes():
    global notes_data
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes_data = json.load(f)
    else:
        notes_data = []

def save_notes():
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_data, f, ensure_ascii=False, indent=2)

# --------------------- MÀN HÌNH ĐĂNG NHẬP ---------------------
def login_screen():
    root.configure(bg="#e8f5e9")
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Đăng nhập", font=("Arial", 18, "bold"), fg="#1b5e20", bg="#e8f5e9").pack(pady=15)

    frame = tk.Frame(root, bg="#e8f5e9")
    frame.pack(pady=10)

    tk.Label(frame, text="Email:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=1, column=1, pady=5)

    def login():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        users = load_users()

        if email in users and users[email] == password:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            main_app(email)
        else:
            messagebox.showerror("Thất bại", "Sai email hoặc mật khẩu.")

    def goto_register():
        register_screen()

    tk.Button(root, text="Đăng nhập", command=login, bg="#43a047", fg="white", font=("Arial", 12), width=20).pack(pady=8)
    tk.Button(root, text="Tạo tài khoản mới", command=goto_register, bg="white", fg="#2e7d32", font=("Arial", 11), width=20, relief="solid").pack()

# --------------------- MÀN HÌNH ĐĂNG KÝ ---------------------
def register_screen():
    root.configure(bg="#e8f5e9")
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Tạo tài khoản", font=("Arial", 18, "bold"), fg="#1b5e20", bg="#e8f5e9").pack(pady=15)

    frame = tk.Frame(root, bg="#e8f5e9")
    frame.pack(pady=10)

    tk.Label(frame, text="Email:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
    email_entry = tk.Entry(frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Mật khẩu:", bg="#e8f5e9", fg="#1b5e20", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
    password_entry.grid(row=1, column=1, pady=5)

    def register():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        users = load_users()

        if email in users:
            messagebox.showerror("Lỗi", "Email đã tồn tại.")
        elif not email or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ.")
        else:
            users[email] = password
            save_users(users)
            messagebox.showinfo("Thành công", "Đăng ký thành công!")
            login_screen()

    tk.Button(root, text="Đăng ký", command=register, bg="#43a047", fg="white", font=("Arial", 12), width=20).pack(pady=8)
    tk.Button(root, text="Quay lại đăng nhập", command=login_screen, bg="white", fg="#2e7d32", font=("Arial", 11), width=20, relief="solid").pack()

# --------------------- HIỂN THỊ GIAO DIỆN TẠO GHI CHÚ (CHỈ FORM) ---------------------
def show_create_note_ui_only(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    content_frame.configure(bg="#252525")

    tk.Label(content_frame, text="Tạo ghi chú mới", bg="#252525", fg="white", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(content_frame, text="Tiêu đề:", bg="#252525", fg="white").pack(anchor="w", padx=10)
    title_entry = tk.Entry(content_frame, font=("Arial", 12))
    title_entry.pack(fill="x", padx=10, pady=5)

    tk.Label(content_frame, text="Nội dung:", bg="#252525", fg="white").pack(anchor="w", padx=10)
    content_text = tk.Text(content_frame, height=15, font=("Arial", 12))
    content_text.pack(fill="both", padx=10, pady=5, expand=True)

    def save_note():
        title = title_entry.get().strip() or "Không tiêu đề"
        content = content_text.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Thiếu nội dung", "Vui lòng nhập nội dung ghi chú.")
            return

        now_str = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        notes_data.insert(0, {
            "title": title,
            "content": content,
            "time": now_str
        })
        save_notes()

        title_entry.delete(0, "end")
        content_text.delete("1.0", "end")
        messagebox.showinfo("Thành công", "Ghi chú đã được lưu.")

    tk.Button(content_frame, text="Lưu ghi chú", bg="#43a047", fg="white", font=("Arial", 12), command=save_note).pack(pady=10)

# --------------------- GIAO DIỆN CHÍNH ---------------------
def main_app(user_email):
    root.geometry("900x600")
    center_window(root, 900, 600)
    root.configure(bg="#1e1e1e")
    for widget in root.winfo_children():
        widget.destroy()

    # Sidebar
    sidebar = tk.Frame(root, bg="#2b2b2b", width=300)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="👤", bg="#2b2b2b", fg="white",
             font=("Arial", 22, "bold")).pack(pady=15)
    tk.Label(sidebar, text=user_email, bg="#2b2b2b", fg="white",
             font=("Arial", 10), wraplength=180).pack(pady=5)

    # Content area
    content_frame = tk.Frame(root, bg="#1e1e1e")
    content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Các hàm hiển thị nội dung khi bấm menu
    def show_home():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Trang chủ", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)


    def show_tasks():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Tasks - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_files():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Files - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_events():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Events - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_tags():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(content_frame, text="Tags - Chức năng đang phát triển", bg="#1e1e1e", fg="white", font=("Arial", 20)).pack(pady=20)

    def show_create_note():
        show_create_note_ui_only(content_frame)

    menu_items = [
        ("Home", show_home),
        ("Tasks", show_tasks),
        ("Files", show_files),
        ("Events", show_events),
        ("Tags", show_tags)
    ]

    for text, command in menu_items:
        tk.Button(sidebar, text=text, command=command, bg="#2b2b2b", fg="white",
                  font=("Arial", 11), relief="flat", anchor="w", padx=20,
                  activebackground="#3a3a3a").pack(fill="x", pady=2)

    tk.Button(sidebar, text="Đăng xuất", command=login_screen,
              bg="#43a047", fg="white", font=("Arial", 11, "bold"),
              relief="flat", pady=8).pack(side="bottom", pady=20, fill="x", padx=10)

    # Mặc định khi đăng nhập hiển thị trang Home
    show_home()

# --------------------- CHẠY CHƯƠNG TRÌNH ---------------------
root = tk.Tk()
root.title("Đăng nhập ứng dụng ghi chú")
root.geometry("420x320")
center_window(root, 420, 320)
login_screen()
root.mainloop()
