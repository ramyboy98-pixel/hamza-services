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
root.minsize(1000, 600)
root.configure(bg="black")

canvas = tk.Canvas(root, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

background_photo = None
normal_icons = {}
large_icons = {}
settings_icons = {}
current_page = "home"


def load_icon(path, size):
    image = Image.open(resource_path(path)).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def draw_background(width, height):
    global background_photo

    bg = Image.open(resource_path("assets/background.jpg")).convert("RGB")
    bg = bg.resize((width, height), Image.LANCZOS)

    dark_layer = Image.new("RGBA", (width, height), (0, 0, 0, 80))
    bg = bg.convert("RGBA")
    bg.alpha_composite(dark_layer)

    background_photo = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")


def show_home():
    global current_page, normal_icons, large_icons
    current_page = "home"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_background(width, height)

    canvas.create_text(
        width // 2,
        int(height * 0.12),
        text="HAMZA SERVICES",
        fill="#f2f2f2",
        font=("Arial", 52, "bold")
    )

    normal_icons = {
        "documents": load_icon("assets/documents.png", (145, 145)),
        "electronic": load_icon("assets/electronic.png", (145, 145)),
        "archive": load_icon("assets/archive.png", (145, 145)),
        "settings": load_icon("assets/settings.png", (145, 145)),
    }

    large_icons = {
        "documents": load_icon("assets/documents.png", (160, 160)),
        "electronic": load_icon("assets/electronic.png", (160, 160)),
        "archive": load_icon("assets/archive.png", (160, 160)),
        "settings": load_icon("assets/settings.png", (160, 160)),
    }

    items = [
        ("documents", "وثائق"),
        ("electronic", "خدمات\nإلكترونية"),
        ("archive", "أرشيف"),
        ("settings", "إعدادات"),
    ]

    positions = [
        width * 0.20,
        width * 0.40,
        width * 0.60,
        width * 0.80,
    ]

    icon_y = height * 0.43
    text_y = height * 0.64

    for index, (key, label) in enumerate(items):
        x = positions[index]

        image_id = canvas.create_image(
            x,
            icon_y,
            image=normal_icons[key],
            anchor="center"
        )

        text_id = canvas.create_text(
            x,
            text_y,
            text=label,
            fill="#f2f2f2",
            font=("Arial", 32, "bold"),
            justify="center"
        )

        def on_enter(event, k=key, img=image_id):
            canvas.itemconfig(img, image=large_icons[k])
            root.config(cursor="hand2")

        def on_leave(event, k=key, img=image_id):
            canvas.itemconfig(img, image=normal_icons[k])
            root.config(cursor="")

        def on_click(event, k=key):
            if k == "settings":
                show_settings()
            else:
                show_placeholder(k)

        canvas.tag_bind(image_id, "<Enter>", on_enter)
        canvas.tag_bind(image_id, "<Leave>", on_leave)
        canvas.tag_bind(image_id, "<Button-1>", on_click)

        canvas.tag_bind(text_id, "<Enter>", on_enter)
        canvas.tag_bind(text_id, "<Leave>", on_leave)
        canvas.tag_bind(text_id, "<Button-1>", on_click)


def show_settings():
    global current_page, settings_icons
    current_page = "settings"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_background(width, height)

    canvas.create_text(
        width // 2,
        int(height * 0.12),
        text="الإعدادات",
        fill="#f2f2f2",
        font=("Arial", 48, "bold")
    )

    settings_icons = {
        "customize": load_icon("assets/customize.png", (90, 90)),
        "backup": load_icon("assets/backup.png", (90, 90)),
        "printer": load_icon("assets/printer.png", (90, 90)),
        "info": load_icon("assets/info.png", (90, 90)),
    }

    items = [
        ("customize", "تخصيص الواجهة"),
        ("backup", "النسخ الاحتياطي"),
        ("printer", "الطباعة\nوالوثائق"),
        ("info", "معلومات البرنامج"),
    ]

    positions = [
        width * 0.20,
        width * 0.40,
        width * 0.60,
        width * 0.80,
    ]

    card_y = height * 0.48

    for index, (key, label) in enumerate(items):
        x = positions[index]

        card = canvas.create_rectangle(
            x - 110,
            card_y - 130,
            x + 110,
            card_y + 130,
            fill="#2a2a2a",
            outline="#555555",
            width=2
        )

        icon_id = canvas.create_image(
            x,
            card_y - 45,
            image=settings_icons[key],
            anchor="center"
        )

        text_id = canvas.create_text(
            x,
            card_y + 70,
            text=label,
            fill="white",
            font=("Arial", 21, "bold"),
            justify="center"
        )

        def on_enter(event, c=card):
            canvas.itemconfig(c, fill="#383838")
            root.config(cursor="hand2")

        def on_leave(event, c=card):
            canvas.itemconfig(c, fill="#2a2a2a")
            root.config(cursor="")

        for item_id in (card, icon_id, text_id):
            canvas.tag_bind(item_id, "<Enter>", on_enter)
            canvas.tag_bind(item_id, "<Leave>", on_leave)

    back_btn = canvas.create_rectangle(
        width // 2 - 80,
        height - 105,
        width // 2 + 80,
        height - 55,
        fill="#404040",
        outline="#666666",
        width=2
    )

    back_text = canvas.create_text(
        width // 2,
        height - 80,
        text="رجوع",
        fill="white",
        font=("Arial", 18, "bold")
    )

    def back_enter(event):
        canvas.itemconfig(back_btn, fill="#555555")
        root.config(cursor="hand2")

    def back_leave(event):
        canvas.itemconfig(back_btn, fill="#404040")
        root.config(cursor="")

    def back_click(event):
        show_home()

    for item_id in (back_btn, back_text):
        canvas.tag_bind(item_id, "<Enter>", back_enter)
        canvas.tag_bind(item_id, "<Leave>", back_leave)
        canvas.tag_bind(item_id, "<Button-1>", back_click)


def show_placeholder(section):
    global current_page
    current_page = section
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_background(width, height)

    titles = {
        "documents": "واجهة الوثائق",
        "electronic": "واجهة الخدمات الإلكترونية",
        "archive": "واجهة الأرشيف",
    }

    canvas.create_text(
        width // 2,
        int(height * 0.18),
        text=titles.get(section, "واجهة جديدة"),
        fill="#f2f2f2",
        font=("Arial", 46, "bold")
    )

    canvas.create_text(
        width // 2,
        int(height * 0.42),
        text="هذه واجهة مؤقتة، سنبني تفاصيلها لاحقًا.",
        fill="#dddddd",
        font=("Arial", 24, "bold")
    )

    back_btn = canvas.create_rectangle(
        width // 2 - 80,
        height - 105,
        width // 2 + 80,
        height - 55,
        fill="#404040",
        outline="#666666",
        width=2
    )

    back_text = canvas.create_text(
        width // 2,
        height - 80,
        text="رجوع",
        fill="white",
        font=("Arial", 18, "bold")
    )

    def back_enter(event):
        canvas.itemconfig(back_btn, fill="#555555")
        root.config(cursor="hand2")

    def back_leave(event):
        canvas.itemconfig(back_btn, fill="#404040")
        root.config(cursor="")

    def back_click(event):
        show_home()

    for item_id in (back_btn, back_text):
        canvas.tag_bind(item_id, "<Enter>", back_enter)
        canvas.tag_bind(item_id, "<Leave>", back_leave)
        canvas.tag_bind(item_id, "<Button-1>", back_click)


def on_resize(event):
    if event.widget == root:
        if current_page == "home":
            show_home()
        elif current_page == "settings":
            show_settings()
        else:
            show_placeholder(current_page)


root.bind("<Configure>", on_resize)

show_home()

root.mainloop()
