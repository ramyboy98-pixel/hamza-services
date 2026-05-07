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
root.title("IDARA DZ")
root.geometry("1280x720")
root.minsize(1000, 600)
root.configure(bg="black")

canvas = tk.Canvas(root, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

background_photo = None
current_page = "home"


def draw_full_background(width, height):
    global background_photo

    path = resource_path("assets/background.jpg")

    if os.path.exists(path):
        img = Image.open(path).convert("RGB")
        img = img.resize((width, height), Image.LANCZOS)
    else:
        img = Image.new("RGB", (width, height), "#173b38")

    background_photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")


def clear_screen():
    canvas.delete("all")


def show_home():
    global current_page
    current_page = "home"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_full_background(width, height)

    right_x = int(width * 0.58)
    menu_center_x = right_x + (width - right_x) // 2

    menu_items = [
        ("وثائق", "documents"),
        ("خدمات إلكترونية", "electronic"),
        ("أرشيف", "archive"),
        ("حول البرنامج", "about"),
    ]

    start_y = int(height * 0.31)
    gap = int(height * 0.135)

    for index, (label, key) in enumerate(menu_items):
        y = start_y + index * gap

        text_id = canvas.create_text(
            menu_center_x,
            y,
            text=label,
            fill="#f4f4f4",
            font=("Arial", 30, "bold"),
            anchor="center"
        )

        hitbox = canvas.create_rectangle(
            right_x + 55,
            y - 35,
            width - 55,
            y + 35,
            fill="",
            outline=""
        )

        def on_enter(event, t=text_id):
            canvas.itemconfig(t, fill="#d7c28a")
            root.config(cursor="hand2")

        def on_leave(event, t=text_id):
            canvas.itemconfig(t, fill="#f4f4f4")
            root.config(cursor="")

        def on_click(event, k=key):
            if k == "about":
                show_about()
            else:
                show_section(k)

        for item in (text_id, hitbox):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)


def draw_back_button(command):
    width = root.winfo_width()
    height = root.winfo_height()

    btn = canvas.create_rectangle(
        35,
        35,
        145,
        82,
        fill="#173b38",
        outline="#d7c28a",
        width=2
    )

    txt = canvas.create_text(
        90,
        58,
        text="رجوع",
        fill="#f4f4f4",
        font=("Arial", 16, "bold")
    )

    def enter(event):
        canvas.itemconfig(btn, fill="#21524d")
        root.config(cursor="hand2")

    def leave(event):
        canvas.itemconfig(btn, fill="#173b38")
        root.config(cursor="")

    def click(event):
        command()

    for item in (btn, txt):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def show_section(section):
    global current_page
    current_page = section
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_full_background(width, height)

    titles = {
        "documents": "وثائق",
        "electronic": "خدمات إلكترونية",
        "archive": "أرشيف",
    }

    canvas.create_rectangle(
        int(width * 0.18),
        int(height * 0.22),
        int(width * 0.82),
        int(height * 0.72),
        fill="#173b38",
        outline="#d7c28a",
        width=2
    )

    canvas.create_text(
        width // 2,
        int(height * 0.34),
        text=titles.get(section, "صفحة"),
        fill="#f4f4f4",
        font=("Arial", 44, "bold")
    )

    canvas.create_text(
        width // 2,
        int(height * 0.50),
        text="سنقوم ببناء هذا القسم لاحقًا.",
        fill="#e8e1d5",
        font=("Arial", 24, "bold")
    )

    draw_back_button(show_home)


def show_about():
    global current_page
    current_page = "about"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_full_background(width, height)

    canvas.create_rectangle(
        int(width * 0.16),
        int(height * 0.18),
        int(width * 0.84),
        int(height * 0.78),
        fill="#173b38",
        outline="#d7c28a",
        width=2
    )

    canvas.create_text(
        width // 2,
        int(height * 0.28),
        text="حول البرنامج",
        fill="#f4f4f4",
        font=("Arial", 42, "bold")
    )

    about_text = (
        "IDARA DZ\n\n"
        "برنامج مكتبي مخصص لتنظيم خدمات المكتبة والخدمات الإدارية.\n"
        "يساعد على تسيير الوثائق، الخدمات الإلكترونية، والأرشيف بطريقة سهلة ومنظمة.\n\n"
        "الإصدار: 1.0.0\n"
        "© 2026"
    )

    canvas.create_text(
        width // 2,
        int(height * 0.50),
        text=about_text,
        fill="#e8e1d5",
        font=("Arial", 22, "bold"),
        justify="center",
        width=int(width * 0.58)
    )

    draw_back_button(show_home)


def on_resize(event):
    if event.widget == root:
        if current_page == "home":
            show_home()
        elif current_page == "about":
            show_about()
        else:
            show_section(current_page)


root.bind("<Configure>", on_resize)

show_home()
root.mainloop()
