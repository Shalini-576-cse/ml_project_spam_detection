import tkinter as tk
from tkinter import messagebox
import pickle
import json

# Load ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Load users
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# Spam prediction
def predict(message):
    vec = vectorizer.transform([message])
    result = model.predict(vec)
    return "Spam" if result[0] == 1 else "Not Spam"

# ---------------- LOGIN SYSTEM ---------------- #

def login():
    username = user_entry.get()
    password = pass_entry.get()

    users = load_users()

    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login Successful!")
        show_main_app()
    else:
        messagebox.showerror("Error", "Invalid Credentials")

def register():
    username = user_entry.get()
    password = pass_entry.get()

    users = load_users()

    if username in users:
        messagebox.showerror("Error", "User already exists")
    else:
        users[username] = password
        save_users(users)
        messagebox.showinfo("Success", "Registered Successfully!")

# ---------------- MAIN APP ---------------- #

def show_main_app():
    login_frame.pack_forget()
    app_frame.pack()

def check_spam():
    message = text_box.get("1.0", tk.END).strip()

    if not message:
        result_label.config(text="Enter a message", fg="orange")
        return

    result = predict(message)

    if result == "Spam":
        result_label.config(text="🚫 Spam", fg="red")
    else:
        result_label.config(text="✅ Not Spam", fg="green")

def clear_text():
    text_box.delete("1.0", tk.END)
    result_label.config(text="")

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Spam Detection System")
root.geometry("450x400")
root.config(bg="#1e1e2f")

# -------- LOGIN FRAME -------- #
login_frame = tk.Frame(root, bg="#1e1e2f")

title = tk.Label(login_frame, text="Login", font=("Arial", 18, "bold"), fg="white", bg="#1e1e2f")
title.pack(pady=10)

user_entry = tk.Entry(login_frame, width=30)
user_entry.pack(pady=5)
user_entry.insert(0, "Username")

pass_entry = tk.Entry(login_frame, width=30, show="*")
pass_entry.pack(pady=5)
pass_entry.insert(0, "Password")

login_btn = tk.Button(login_frame, text="Login", command=login, bg="#4CAF50", fg="white", width=10)
login_btn.pack(pady=5)

register_btn = tk.Button(login_frame, text="Register", command=register, bg="#2196F3", fg="white", width=10)
register_btn.pack(pady=5)

login_frame.pack(pady=50)

# -------- MAIN APP FRAME -------- #
app_frame = tk.Frame(root, bg="#1e1e2f")

app_title = tk.Label(app_frame, text="Spam Detector", font=("Arial", 16, "bold"), fg="white", bg="#1e1e2f")
app_title.pack(pady=10)

text_box = tk.Text(app_frame, height=5, width=40)
text_box.pack(pady=10)

check_btn = tk.Button(app_frame, text="Check", command=check_spam, bg="#ff9800", fg="white", width=10)
check_btn.pack(pady=5)

clear_btn = tk.Button(app_frame, text="Clear", command=clear_text, bg="#f44336", fg="white", width=10)
clear_btn.pack(pady=5)

result_label = tk.Label(app_frame, text="", font=("Arial", 14), bg="#1e1e2f")
result_label.pack(pady=10)

root.mainloop()

root = tk.Tk()
root.lift()
root.attributes('-topmost', True)
root.after(100, lambda: root.attributes('-topmost', False))