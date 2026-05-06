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
icon_photos = {}
normal_icons = {}
large_icons = {}
current_hover = None


def load_icon(path, size):
    image = Image.open(resource_path(path)).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def open_section(name):
    print(f"Open: {name}")


def draw_interface():
    global background_photo, icon_photos, normal_icons, large_icons, current_hover

    current_hover = None
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    bg = Image.open(resource_path("assets/background.jpg")).convert("RGB")
    bg = bg.resize((width, height), Image.LANCZOS)

    dark_layer = Image.new("RGBA", (width, height), (0, 0, 0, 75))
    bg = bg.convert("RGBA")
    bg.alpha_composite(dark_layer)

    background_photo = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")

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

    icon_photos = normal_icons

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
            anchor="center",
            tags=(key, "menu_item")
        )

        text_id = canvas.create_text(
            x,
            text_y,
            text=label,
            fill="#f2f2f2",
            font=("Arial", 32, "bold"),
            justify="center",
            tags=(key, "menu_item")
        )

        def on_enter(event, k=key, img=image_id):
            global current_hover
            current_hover = k
            canvas.itemconfig(img, image=large_icons[k])
            root.config(cursor="hand2")

        def on_leave(event, k=key, img=image_id):
            global current_hover
            current_hover = None
            canvas.itemconfig(img, image=normal_icons[k])
            root.config(cursor="")

        def on_click(event, k=key):
            open_section(k)

        canvas.tag_bind(image_id, "<Enter>", on_enter)
        canvas.tag_bind(image_id, "<Leave>", on_leave)
        canvas.tag_bind(image_id, "<Button-1>", on_click)

        canvas.tag_bind(text_id, "<Enter>", on_enter)
        canvas.tag_bind(text_id, "<Leave>", on_leave)
        canvas.tag_bind(text_id, "<Button-1>", on_click)


def on_resize(event):
    if event.widget == root:
        draw_interface()


root.bind("<Configure>", on_resize)

draw_interface()

root.mainloop()
