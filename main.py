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


def load_icon(path, size):
    image = Image.open(resource_path(path)).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def open_section(name):

    if name == "settings":

        page = tk.Toplevel(root)
        page.title("الإعدادات")
        page.geometry("1200x720")
        page.configure(bg="#181818")

        title = tk.Label(
            page,
            text="الإعدادات",
            font=("Arial", 38, "bold"),
            fg="white",
            bg="#181818"
        )
        title.pack(pady=35)

        cards_frame = tk.Frame(page, bg="#181818")
        cards_frame.pack(expand=True)

        global settings_icons

        settings_icons = {
            "customize": load_icon("assets/customize.png", (90, 90)),
            "backup": load_icon("assets/backup.png", (90, 90)),
            "printer": load_icon("assets/printer.png", (90, 90)),
            "info": load_icon("assets/info.png", (90, 90)),
        }

        settings_items = [
            ("customize", "تخصيص الواجهة"),
            ("backup", "النسخ الاحتياطي"),
            ("printer", "الطباعة\nوالوثائق"),
            ("info", "معلومات البرنامج")
        ]

        for key, text in settings_items:

            card = tk.Frame(
                cards_frame,
                bg="#2a2a2a",
                width=230,
                height=260,
                highlightthickness=2,
                highlightbackground="#3d3d3d"
            )

            card.pack(side="left", padx=25)
            card.pack_propagate(False)

            icon = tk.Label(
                card,
                image=settings_icons[key],
                bg="#2a2a2a"
            )
            icon.pack(pady=(25, 15))

            label = tk.Label(
                card,
                text=text,
                font=("Arial", 20, "bold"),
                fg="white",
                bg="#2a2a2a",
                wraplength=180,
                justify="center"
            )
            label.pack(expand=True)

            def enter_effect(event, target=card):
                target.config(bg="#353535")

            def leave_effect(event, target=card):
                target.config(bg="#2a2a2a")

            card.bind("<Enter>", enter_effect)
            card.bind("<Leave>", leave_effect)

            icon.bind("<Enter>", enter_effect)
            icon.bind("<Leave>", leave_effect)

            label.bind("<Enter>", enter_effect)
            label.bind("<Leave>", leave_effect)

        back_btn = tk.Button(
            page,
            text="رجوع",
            font=("Arial", 16, "bold"),
            bg="#404040",
            fg="white",
            activebackground="#5a5a5a",
            activeforeground="white",
            relief="flat",
            padx=28,
            pady=12,
            command=page.destroy
        )

        back_btn.pack(pady=35)

        return

    titles = {
        "documents": "واجهة الوثائق",
        "electronic": "واجهة الخدمات الإلكترونية",
        "archive": "واجهة الأرشيف",
    }

    page = tk.Toplevel(root)
    page.title(titles.get(name, "واجهة جديدة"))
    page.geometry("900x600")
    page.configure(bg="#1f1f1f")

    title = tk.Label(
        page,
        text=titles.get(name, "واجهة جديدة"),
        font=("Arial", 32, "bold"),
        fg="white",
        bg="#1f1f1f"
    )
    title.pack(pady=40)

    note = tk.Label(
        page,
        text="هذه واجهة مؤقتة، سنبني تفاصيلها لاحقًا.",
        font=("Arial", 18),
        fg="#dddddd",
        bg="#1f1f1f"
    )
    note.pack(pady=20)

    close_btn = tk.Button(
        page,
        text="إغلاق",
        font=("Arial", 16, "bold"),
        bg="#3a3a3a",
        fg="white",
        activebackground="#555555",
        activeforeground="white",
        relief="flat",
        padx=25,
        pady=10,
        command=page.destroy
    )
    close_btn.pack(pady=40)


def draw_interface():
    global background_photo, normal_icons, large_icons

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

    canvas.create_image(
        0,
        0,
        image=background_photo,
        anchor="nw"
    )

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
