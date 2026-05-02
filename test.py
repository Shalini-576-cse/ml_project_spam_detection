import tkinter as tk

print("Starting...")

root = tk.Tk()
root.title("Test Window")
root.geometry("300x200+200+200")

label = tk.Label(root, text="Hello!")
label.pack()

root.mainloop()