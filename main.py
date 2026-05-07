import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import shutil


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
current_page = "home"

BACKGROUND_FILE = "assets/background.jpg"


def load_icon(path, size):
    image = Image.open(resource_path(path)).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def make_setting_icon(color, symbol, size=58):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, size, size), radius=14, fill=color)

    try:
        font = ("Arial", int(size * 0.45), "bold")
    except:
        font = None

    return ImageTk.PhotoImage(img)


def draw_background(width, height):
    global background_photo

    bg = Image.open(resource_path(BACKGROUND_FILE)).convert("RGB")
    bg = bg.resize((width, height), Image.LANCZOS)

    dark_layer = Image.new("RGBA", (width, height), (0, 0, 0, 170))
    bg = bg.convert("RGBA")
    bg.alpha_composite(dark_layer)

    background_photo = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")


def change_background():
    file_path = filedialog.askopenfilename(
        title="اختر صورة خلفية",
        filetypes=[("Images", "*.png *.jpg *.jpeg")]
    )

    if not file_path:
        return

    try:
        shutil.copy(file_path, BACKGROUND_FILE)
        show_customize()
    except Exception as e:
        print(e)


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

    positions = [width * 0.20, width * 0.40, width * 0.60, width * 0.80]
    icon_y = height * 0.43
    text_y = height * 0.64

    for index, (key, label) in enumerate(items):
        x = positions[index]

        image_id = canvas.create_image(x, icon_y, image=normal_icons[key], anchor="center")
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

        for item in (image_id, text_id):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)


def show_settings():
    global current_page
    current_page = "settings"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()
    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_background(width, height)

    canvas.create_text(
        35,
        28,
        text="HAMZA SERVICES",
        fill="#eeeeee",
        font=("Arial", 14, "bold"),
        anchor="w"
    )

    back_box = canvas.create_rectangle(
        35, 60, 125, 105,
        fill="#242428",
        outline="#34343a",
        width=1
    )

    back_text = canvas.create_text(
        80, 82,
        text="←  رجوع",
        fill="white",
        font=("Arial", 16, "bold")
    )

    def back_enter(event):
        canvas.itemconfig(back_box, fill="#303036")
        root.config(cursor="hand2")

    def back_leave(event):
        canvas.itemconfig(back_box, fill="#242428")
        root.config(cursor="")

    def back_click(event):
        show_home()

    for item in (back_box, back_text):
        canvas.tag_bind(item, "<Enter>", back_enter)
        canvas.tag_bind(item, "<Leave>", back_leave)
        canvas.tag_bind(item, "<Button-1>", back_click)

    canvas.create_text(
        width // 2,
        82,
        text="الإعدادات",
        fill="white",
        font=("Arial", 38, "bold")
    )

    settings_items = [
        ("🔐", "#2f7df6", "الحساب والأمان", "تغيير اسم المستخدم وكلمة المرور وإعدادات الأمان", "account"),
        ("🎨", "#8d3ff2", "تخصيص الواجهة", "تغيير الخلفية والألوان والخطوط والمظهر العام", "customize"),
        ("🖨", "#55b72c", "الطباعة", "إعدادات الطابعة ومعاينة قبل الطباعة", "printer"),
        ("📄", "#ff8a18", "إدارة الوثائق", "إعدادات حفظ الوثائق والقوالب والتنسيقات", "documents_settings"),
        ("🛡", "#25b7b1", "النسخ الاحتياطي والحماية", "النسخ الاحتياطي واسترجاع البيانات وإعدادات الحماية", "backup"),
        ("👥", "#e03c78", "قاعدة بيانات الزبائن", "إعدادات قاعدة البيانات والبحث والتصدير والاستيراد", "clients_db"),
        ("⚡", "#ffcf00", "الذكاء والسرعة", "الخيارات الذكية والاختصارات والاقتراحات", "smart"),
        ("ℹ", "#2da7ff", "معلومات البرنامج", "معلومات الإصدار والتحديثات والمطور", "info"),
    ]

    list_x1 = int(width * 0.10)
    list_x2 = int(width * 0.90)
    start_y = 130
    row_h = 74
    gap = 8

    for i, (symbol, color, title, desc, key) in enumerate(settings_items):
        y1 = start_y + i * (row_h + gap)
        y2 = y1 + row_h

        card = canvas.create_rectangle(
            list_x1, y1, list_x2, y2,
            fill="#202024",
            outline="#34343a",
            width=1
        )

        icon_bg = canvas.create_rectangle(
            list_x1 + 28, y1 + 12,
            list_x1 + 78, y1 + 62,
            fill=color,
            outline=color,
            width=1
        )

        icon_text = canvas.create_text(
            list_x1 + 53,
            y1 + 37,
            text=symbol,
            fill="white",
            font=("Arial", 23, "bold")
        )

        title_text = canvas.create_text(
            list_x1 + 115,
            y1 + 25,
            text=title,
            fill="white",
            font=("Arial", 19, "bold"),
            anchor="w"
        )

        desc_text = canvas.create_text(
            list_x1 + 115,
            y1 + 52,
            text=desc,
            fill="#bdbdbd",
            font=("Arial", 12),
            anchor="w"
        )

        arrow = canvas.create_text(
            list_x2 - 38,
            y1 + 37,
            text="›",
            fill="#cfcfcf",
            font=("Arial", 42, "bold")
        )

        def on_enter(event, c=card):
            canvas.itemconfig(c, fill="#29292f")
            root.config(cursor="hand2")

        def on_leave(event, c=card):
            canvas.itemconfig(c, fill="#202024")
            root.config(cursor="")

        def on_click(event, k=key):
            if k == "customize":
                show_customize()
            else:
                show_setting_placeholder(k)

        for item in (card, icon_bg, icon_text, title_text, desc_text, arrow):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)


def show_customize():
    global current_page
    current_page = "customize"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)

    canvas.create_text(
        width // 2,
        85,
        text="تخصيص الواجهة",
        fill="white",
        font=("Arial", 38, "bold")
    )

    buttons = [
        ("تغيير صورة الخلفية", "اختر صورة من الحاسوب واستعملها كخلفية للبرنامج", 230, change_background),
        ("إعادة ضبط المصنع", "إرجاع إعدادات البرنامج إلى الوضع الافتراضي دون حذف البيانات", 330, None),
    ]

    for title, desc, y, command in buttons:
        box = canvas.create_rectangle(
            width // 2 - 300,
            y,
            width // 2 + 300,
            y + 82,
            fill="#202024",
            outline="#34343a",
            width=1
        )

        title_id = canvas.create_text(
            width // 2 - 260,
            y + 28,
            text=title,
            fill="white",
            font=("Arial", 20, "bold"),
            anchor="w"
        )

        desc_id = canvas.create_text(
            width // 2 - 260,
            y + 57,
            text=desc,
            fill="#bdbdbd",
            font=("Arial", 12),
            anchor="w"
        )

        arrow = canvas.create_text(
            width // 2 + 260,
            y + 41,
            text="›",
            fill="#cfcfcf",
            font=("Arial", 42, "bold")
        )

        def enter(event, b=box):
            canvas.itemconfig(b, fill="#29292f")
            root.config(cursor="hand2")

        def leave(event, b=box):
            canvas.itemconfig(b, fill="#202024")
            root.config(cursor="")

        def click(event, cmd=command):
            if cmd:
                cmd()

        for item in (box, title_id, desc_id, arrow):
            canvas.tag_bind(item, "<Enter>", enter)
            canvas.tag_bind(item, "<Leave>", leave)
            canvas.tag_bind(item, "<Button-1>", click)

    draw_back_button(show_settings)


def show_setting_placeholder(key):
    global current_page
    current_page = key
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)

    titles = {
        "account": "الحساب والأمان",
        "printer": "الطباعة",
        "documents_settings": "إدارة الوثائق",
        "backup": "النسخ الاحتياطي والحماية",
        "clients_db": "قاعدة بيانات الزبائن",
        "smart": "الذكاء والسرعة",
        "info": "معلومات البرنامج",
    }

    canvas.create_text(
        width // 2,
        120,
        text=titles.get(key, "قسم الإعدادات"),
        fill="white",
        font=("Arial", 40, "bold")
    )

    canvas.create_text(
        width // 2,
        300,
        text="سنقوم ببناء هذا القسم لاحقًا.",
        fill="#dddddd",
        font=("Arial", 24, "bold")
    )

    draw_back_button(show_settings)


def show_placeholder(section):
    global current_page
    current_page = section
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)

    titles = {
        "documents": "واجهة الوثائق",
        "electronic": "واجهة الخدمات الإلكترونية",
        "archive": "واجهة الأرشيف",
    }

    canvas.create_text(
        width // 2,
        140,
        text=titles.get(section, "واجهة جديدة"),
        fill="white",
        font=("Arial", 46, "bold")
    )

    canvas.create_text(
        width // 2,
        320,
        text="هذه واجهة مؤقتة، سنبني تفاصيلها لاحقًا.",
        fill="#dddddd",
        font=("Arial", 24, "bold")
    )

    draw_back_button(show_home)


def draw_back_button(command):
    width = root.winfo_width()
    height = root.winfo_height()

    btn = canvas.create_rectangle(
        width // 2 - 90,
        height - 82,
        width // 2 + 90,
        height - 32,
        fill="#404040",
        outline="#666666",
        width=1
    )

    txt = canvas.create_text(
        width // 2,
        height - 57,
        text="رجوع",
        fill="white",
        font=("Arial", 18, "bold")
    )

    def enter(event):
        canvas.itemconfig(btn, fill="#555555")
        root.config(cursor="hand2")

    def leave(event):
        canvas.itemconfig(btn, fill="#404040")
        root.config(cursor="")

    def click(event):
        command()

    for item in (btn, txt):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def on_resize(event):
    if event.widget == root:
        if current_page == "home":
            show_home()
        elif current_page == "settings":
            show_settings()
        elif current_page == "customize":
            show_customize()
        elif current_page in [
            "account", "printer", "documents_settings", "backup",
            "clients_db", "smart", "info"
        ]:
            show_setting_placeholder(current_page)
        else:
            show_placeholder(current_page)


root.bind("<Configure>", on_resize)

show_home()

root.mainloop()
