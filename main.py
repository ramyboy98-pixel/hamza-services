import tkinter as tk
from PIL import Image, ImageTk
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = tk.Tk()

root.title("HAMZA SERVICES")
root.geometry("1280x720")
root.configure(bg="black")


bg_path = resource_path("assets/background.jpg")

bg_image = Image.open(bg_path)
bg_image = bg_image.resize((1280, 720))

bg_photo = ImageTk.PhotoImage(bg_image)


canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")


canvas.create_text(
    640,
    70,
    text="HAMZA SERVICES",
    fill="white",
    font=("Arial", 42, "bold")
)


items = [
    ("وثائق", 220),
    ("خدمات إلكترونية", 500),
    ("أرشيف", 780),
    ("إعدادات", 1060),
]


for text, x in items:

    card = tk.Frame(
        root,
        bg="#2f2f2f",
        width=180,
        height=180
    )

    card.pack_propagate(False)

    label = tk.Label(
        card,
        text=text,
        fg="white",
        bg="#2f2f2f",
        font=("Arial", 22, "bold"),
        wraplength=160,
        justify="center"
    )

    label.pack(expand=True)

    canvas.create_window(
        x,
        360,
        window=card
    )


root.mainloop()
