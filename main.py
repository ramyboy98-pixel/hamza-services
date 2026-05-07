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
animation_running = False


def clear_screen():
    global animation_running
    animation_running = False
    canvas.delete("all")


def draw_image(path, width, height):
    global background_photo

    if os.path.exists(path):
        img = Image.open(path).convert("RGB")
        img = img.resize((width, height), Image.LANCZOS)
    else:
        img = Image.new("RGB", (width, height), "#173b38")

    background_photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")


def show_home():
    global current_page
    current_page = "home"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

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
            elif k == "documents":
                show_documents()
            else:
                show_section(k)

        for item in (text_id, hitbox):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)


def draw_back_button(command):
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


def show_documents():
    global current_page, animation_running
    current_page = "documents"
    clear_screen()
    animation_running = True

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    right_x = int(width * 0.58)
    menu_center_x = right_x + (width - right_x) // 2

    title_start_y = int(height * 0.31)
    title_target_y = int(height * 0.15)

    title_id = canvas.create_text(
        menu_center_x,
        title_start_y,
        text="وثائق",
        fill="#f4f4f4",
        font=("Arial", 30, "bold"),
        anchor="center"
    )

    sub_items = [
        ("طلب خطي", "written_request"),
        ("تصريح شرفي", "honor_statement"),
        ("سيرة ذاتية", "cv"),
        ("فاتورة", "invoice"),
    ]

    sub_texts = []
    line_ids = []

    start_y = int(height * 0.31)
    gap = int(height * 0.135)

    for index, (label, key) in enumerate(sub_items):
        y = start_y + index * gap
        start_x = width + 240
        target_x = menu_center_x

        text_id = canvas.create_text(
            start_x,
            y,
            text=label,
            fill="#e8e1d5",
            font=("Arial", 24, "bold"),
            anchor="center"
        )

        line_id = canvas.create_line(
            width + 100,
            y + int(gap * 0.43),
            width + 520,
            y + int(gap * 0.43),
            fill="#8aa09c",
            width=1
        )

        sub_texts.append((text_id, key, target_x, y))
        line_ids.append((line_id, right_x + 70, width - 70, y + int(gap * 0.43)))

    def animate_title(step=0):
        if not animation_running or current_page != "documents":
            return

        total_steps = 16
        if step <= total_steps:
            current_y = title_start_y + (title_target_y - title_start_y) * step / total_steps
            size = int(30 + (54 - 30) * step / total_steps)
            canvas.coords(title_id, menu_center_x, current_y)
            canvas.itemconfig(title_id, font=("Arial", size, "bold"))
            root.after(18, lambda: animate_title(step + 1))
        else:
            animate_sub_items(0)

    def animate_sub_items(step=0):
        if not animation_running or current_page != "documents":
            return

        total_steps = 22
        if step <= total_steps:
            for text_id, key, target_x, y in sub_texts:
                start_x = width + 240
                current_x = start_x + (target_x - start_x) * step / total_steps
                canvas.coords(text_id, current_x, y)

            for line_id, x1, x2, y in line_ids:
                start_x1 = width + 100
                start_x2 = width + 520
                current_x1 = start_x1 + (x1 - start_x1) * step / total_steps
                current_x2 = start_x2 + (x2 - start_x2) * step / total_steps
                canvas.coords(line_id, current_x1, y, current_x2, y)

            root.after(16, lambda: animate_sub_items(step + 1))
        else:
            bind_document_items()

    def bind_document_items():
        for text_id, key, target_x, y in sub_texts:
            hitbox = canvas.create_rectangle(
                right_x + 55,
                y - 32,
                width - 55,
                y + 32,
                fill="",
                outline=""
            )

            def on_enter(event, t=text_id):
                canvas.itemconfig(t, fill="#d7c28a")
                root.config(cursor="hand2")

            def on_leave(event, t=text_id):
                canvas.itemconfig(t, fill="#e8e1d5")
                root.config(cursor="")

            def on_click(event, k=key):
                show_document_type(k)

            for item in (text_id, hitbox):
                canvas.tag_bind(item, "<Enter>", on_enter)
                canvas.tag_bind(item, "<Leave>", on_leave)
                canvas.tag_bind(item, "<Button-1>", on_click)

        draw_back_button(show_home)

    animate_title()


def show_document_type(doc_type):
    global current_page
    current_page = doc_type
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    titles = {
        "written_request": "طلب خطي",
        "honor_statement": "تصريح شرفي",
        "cv": "سيرة ذاتية",
        "invoice": "فاتورة",
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
        text=titles.get(doc_type, "وثيقة"),
        fill="#f4f4f4",
        font=("Arial", 44, "bold")
    )

    canvas.create_text(
        width // 2,
        int(height * 0.50),
        text="سنقوم ببناء هذه الوثيقة في الخطوة القادمة.",
        fill="#e8e1d5",
        font=("Arial", 24, "bold")
    )

    draw_back_button(show_documents)


def show_section(section):
    global current_page
    current_page = section
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    titles = {
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

    draw_image(resource_path("assets/about.jpg"), width, height)

    draw_back_button(show_home)


def on_resize(event):
    if event.widget == root:
        if current_page == "home":
            show_home()
        elif current_page == "about":
            show_about()
        elif current_page == "documents":
            show_documents()
        elif current_page in ["written_request", "honor_statement", "cv", "invoice"]:
            show_document_type(current_page)
        else:
            show_section(current_page)


root.bind("<Configure>", on_resize)

show_home()
root.mainloop()
