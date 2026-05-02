import tkinter as tk
import pickle

# Load trained model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def check_spam():
    message = entry.get()

    if message.strip() == "":
        result_label.config(text="Please enter a message", fg="orange")
        return

    vec = vectorizer.transform([message])
    result = model.predict(vec)

    if result[0] == 1:
        result_label.config(text="🚫 Spam", fg="red")
    else:
        result_label.config(text="✅ Not Spam", fg="green")

# Create window
root = tk.Tk()
root.title("Spam Email Detector")
root.geometry("400x250")
root.resizable(False, False)

# Title
title = tk.Label(root, text="Spam Detection System", font=("Arial", 16, "bold"))
title.pack(pady=10)

# Input box
entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=10)

# Button
check_btn = tk.Button(root, text="Check Message", command=check_spam, bg="blue", fg="white")
check_btn.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

# Run app
root.mainloop()