import tkinter as tk

root = tk.Tk()

root.title("HAMZA SERVICES")
root.geometry("1280x720")
root.configure(bg="#2b2b2b")

title = tk.Label(
    root,
    text="HAMZA SERVICES",
    font=("Arial", 36, "bold"),
    fg="white",
    bg="#2b2b2b"
)
title.pack(pady=40)

frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(expand=True)

buttons = [
    "وثائق",
    "خدمات إلكترونية",
    "أرشيف",
    "إعدادات"
]

for text in buttons:
    card = tk.Frame(
        frame,
        bg="#3a3a3a",
        width=220,
        height=220
    )
    card.pack(side="left", padx=25)

    card.pack_propagate(False)

    label = tk.Label(
        card,
        text=text,
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#3a3a3a"
    )
    label.pack(expand=True)

root.mainloop()
