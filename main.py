import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import shutil
import json


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


APP_DATA_DIR = os.path.join(os.path.expanduser("~"), "HamzaServices")
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
CUSTOM_BACKGROUND = os.path.join(APP_DATA_DIR, "background.jpg")
CLIENTS_FILE = os.path.join(APP_DATA_DIR, "clients.json")

DEFAULT_SETTINGS = {
    "username": "admin",
    "password": "1234",
    "background": "",
    "theme": "dark",
    "accent_color": "#ffa51f",
    "font_size": "medium",
    "effects": True,
    "printer_name": "الطابعة الافتراضية",
    "color_printing": True,
    "print_preview": True,
    "save_pdf": True,
    "clients_count": 0
}

ACCENT_COLORS = {
    "برتقالي": "#ffa51f",
    "أزرق": "#2f7df6",
    "بنفسجي": "#8d3ff2",
    "أخضر": "#22c55e",
    "أحمر": "#ef4444",
    "ذهبي": "#facc15"
}

FONT_SIZES = {
    "small": {"title": 40, "subtitle": 18, "menu": 24, "button": 16, "normal": 14, "small": 11},
    "medium": {"title": 52, "subtitle": 22, "menu": 32, "button": 18, "normal": 16, "small": 12},
    "large": {"title": 62, "subtitle": 26, "menu": 38, "button": 22, "normal": 20, "small": 14}
}

os.makedirs(APP_DATA_DIR, exist_ok=True)


def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, value in DEFAULT_SETTINGS.items():
            data.setdefault(key, value)

        return data
    except:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


settings = load_settings()


def load_clients():
    if not os.path.exists(CLIENTS_FILE):
        save_clients([])
        return []

    try:
        with open(CLIENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data

        return []
    except:
        save_clients([])
        return []


def save_clients(clients):
    with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(clients, f, ensure_ascii=False, indent=4)


clients_data = load_clients()


def refresh_clients_count():
    settings["clients_count"] = len(clients_data)
    save_settings(settings)



def get_fonts():
    return FONT_SIZES.get(settings.get("font_size", "medium"), FONT_SIZES["medium"])


def get_accent():
    return settings.get("accent_color", "#ffa51f")


def get_theme():
    accent = get_accent()

    if settings.get("theme") == "light":
        return {
            "overlay": 95,
            "card": "#f2f2f2",
            "card_hover": "#ffffff",
            "border": "#d0d0d0",
            "text": "#111111",
            "muted": "#444444",
            "button": "#dddddd",
            "button_hover": "#ffffff",
            "accent": accent
        }

    return {
        "overlay": 170,
        "card": "#202024",
        "card_hover": "#29292f",
        "border": "#34343a",
        "text": "#ffffff",
        "muted": "#bdbdbd",
        "button": "#404040",
        "button_hover": "#555555",
        "accent": accent
    }


root = tk.Tk()
root.title("HAMZA SERVICES")
root.geometry("1280x720")
root.minsize(1000, 600)
root.configure(bg="black")

canvas = tk.Canvas(root, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

background_photo = None
login_photo = None
normal_icons = {}
large_icons = {}
current_page = "login"
entry_widgets = []


def clear_entries():
    global entry_widgets
    for widget in entry_widgets:
        try:
            widget.destroy()
        except:
            pass
    entry_widgets = []


def load_icon(path, size):
    image = Image.open(resource_path(path)).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def get_background_path():
    if settings.get("background") and os.path.exists(settings["background"]):
        return settings["background"]
    return resource_path("assets/background.jpg")


def draw_background(width, height):
    global background_photo
    theme = get_theme()

    bg = Image.open(get_background_path()).convert("RGB")
    bg = bg.resize((width, height), Image.LANCZOS)

    layer = Image.new("RGBA", (width, height), (0, 0, 0, theme["overlay"]))
    bg = bg.convert("RGBA")
    bg.alpha_composite(layer)

    background_photo = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")


def draw_login_background(width, height):
    global login_photo

    path = resource_path("assets/login_background.jpg")
    if not os.path.exists(path):
        path = resource_path("assets/background.jpg")

    bg = Image.open(path).convert("RGB")
    bg = bg.resize((width, height), Image.LANCZOS)

    layer = Image.new("RGBA", (width, height), (0, 0, 0, 85))
    bg = bg.convert("RGBA")
    bg.alpha_composite(layer)

    login_photo = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=login_photo, anchor="nw")


def change_background():
    file_path = filedialog.askopenfilename(
        title="اختر صورة خلفية",
        filetypes=[("Images", "*.png *.jpg *.jpeg")]
    )

    if not file_path:
        return

    shutil.copy(file_path, CUSTOM_BACKGROUND)
    settings["background"] = CUSTOM_BACKGROUND
    save_settings(settings)
    show_customize()


def set_theme(value):
    settings["theme"] = value
    save_settings(settings)
    show_customize()


def set_accent_color(color):
    settings["accent_color"] = color
    save_settings(settings)
    show_accent_colors()


def set_font_size(size):
    settings["font_size"] = size
    save_settings(settings)
    show_font_sizes()


def toggle_effects():
    settings["effects"] = not settings.get("effects", True)
    save_settings(settings)
    show_customize()


def reset_factory():
    settings["background"] = ""
    settings["theme"] = "dark"
    settings["accent_color"] = "#ffa51f"
    settings["font_size"] = "medium"
    settings["effects"] = True
    save_settings(settings)
    messagebox.showinfo("تم", "تمت إعادة ضبط إعدادات الواجهة.")
    show_customize()


def toggle_color_printing():
    settings["color_printing"] = not settings.get("color_printing", True)
    save_settings(settings)
    show_printer_settings()


def toggle_print_preview():
    settings["print_preview"] = not settings.get("print_preview", True)
    save_settings(settings)
    show_printer_settings()


def toggle_save_pdf():
    settings["save_pdf"] = not settings.get("save_pdf", True)
    save_settings(settings)
    show_printer_settings()


def draw_top_back(title, back_command):
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()

    canvas.create_text(
        35,
        28,
        text="HAMZA SERVICES",
        fill=theme["text"],
        font=("Arial", fonts["normal"], "bold"),
        anchor="w"
    )

    back_box = canvas.create_rectangle(
        35,
        60,
        125,
        105,
        fill=theme["button"],
        outline=theme["border"],
        width=1
    )

    back_text = canvas.create_text(
        80,
        82,
        text="←  رجوع",
        fill=theme["text"],
        font=("Arial", fonts["normal"], "bold")
    )

    canvas.create_text(
        width // 2,
        82,
        text=title,
        fill=theme["text"],
        font=("Arial", fonts["title"] - 14, "bold")
    )

    def enter(event):
        if settings.get("effects", True):
            canvas.itemconfig(back_box, fill=theme["button_hover"])
        root.config(cursor="hand2")

    def leave(event):
        if settings.get("effects", True):
            canvas.itemconfig(back_box, fill=theme["button"])
        root.config(cursor="")

    def click(event):
        back_command()

    for item in (back_box, back_text):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def draw_list(items, on_click_func):
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()

    list_x1 = int(width * 0.10)
    list_x2 = int(width * 0.90)
    start_y = 130
    row_h = 74
    gap = 8

    for i, (symbol, color, title, desc, key) in enumerate(items):
        y1 = start_y + i * (row_h + gap)
        y2 = y1 + row_h

        card = canvas.create_rectangle(
            list_x1, y1, list_x2, y2,
            fill=theme["card"],
            outline=theme["border"],
            width=1
        )

        icon_bg = canvas.create_rectangle(
            list_x1 + 28, y1 + 12,
            list_x1 + 78, y1 + 62,
            fill=color,
            outline=color
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
            fill=theme["text"],
            font=("Arial", fonts["button"], "bold"),
            anchor="w"
        )

        desc_text = canvas.create_text(
            list_x1 + 115,
            y1 + 52,
            text=desc,
            fill=theme["muted"],
            font=("Arial", fonts["small"]),
            anchor="w"
        )

        arrow = canvas.create_text(
            list_x2 - 38,
            y1 + 37,
            text="›",
            fill=theme["muted"],
            font=("Arial", 42, "bold")
        )

        def on_enter(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card_hover"])
            root.config(cursor="hand2")

        def on_leave(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card"])
            root.config(cursor="")

        def click(event, k=key):
            on_click_func(k)

        for item in (card, icon_bg, icon_text, title_text, desc_text, arrow):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", click)


def show_login():
    global current_page
    clear_entries()
    current_page = "login"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    accent = theme["accent"]

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_login_background(width, height)

    center_x = width // 2

    canvas.create_text(center_x, int(height * 0.19), text="Hamza services",
                       fill="black", font=("Segoe Script", fonts["title"] + 6, "bold"))

    canvas.create_text(center_x, int(height * 0.30), text="user name",
                       fill="white", font=("Courier New", fonts["subtitle"] + 3, "bold"))

    username_entry = tk.Entry(root, font=("Courier New", fonts["subtitle"] + 4, "bold"),
                              justify="center", bd=0, bg=accent, fg="black",
                              insertbackground="black")
    username_entry.insert(0, settings.get("username", "admin"))

    canvas.create_window(center_x, int(height * 0.37), window=username_entry, width=360, height=48)

    canvas.create_text(center_x, int(height * 0.45), text="password",
                       fill="white", font=("Courier New", fonts["subtitle"] + 3, "bold"))

    password_entry = tk.Entry(root, font=("Courier New", fonts["subtitle"] + 4, "bold"),
                              justify="center", show="*", bd=0, bg=accent, fg="black",
                              insertbackground="black")

    canvas.create_window(center_x, int(height * 0.52), window=password_entry, width=360, height=48)

    entry_widgets.extend([username_entry, password_entry])

    login_btn = canvas.create_rectangle(center_x - 170, int(height * 0.64),
                                        center_x + 170, int(height * 0.64) + 62,
                                        fill=accent, outline=accent, width=3)

    login_text = canvas.create_text(center_x, int(height * 0.64) + 31,
                                    text="LOGIN", fill="black",
                                    font=("Courier New", fonts["subtitle"] + 5, "bold"))

    error_text = canvas.create_text(center_x, int(height * 0.75), text="",
                                    fill="#ff4b4b",
                                    font=("Arial", fonts["normal"], "bold"))

    forgot_text = canvas.create_text(center_x, int(height * 0.81), text="نسيت كلمة السر؟",
                                     fill="#ffffff",
                                     font=("Arial", fonts["normal"] + 1, "bold"))

    canvas.create_line(int(width * 0.18), int(height * 0.88),
                       int(width * 0.82), int(height * 0.88), fill="#777777")

    canvas.create_text(center_x, int(height * 0.94),
                       text="🔒 الرجاء إدخال اسم المستخدم وكلمة المرور للدخول",
                       fill="white", font=("Arial", fonts["normal"] + 2, "bold"))

    def do_login(event=None):
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == settings.get("username") and password == settings.get("password"):
            show_home()
        else:
            canvas.itemconfig(error_text, text="اسم المستخدم أو كلمة المرور غير صحيحة")

    def forgot_enter(event):
        if settings.get("effects", True):
            canvas.itemconfig(forgot_text, fill=accent)
        root.config(cursor="hand2")

    def forgot_leave(event):
        if settings.get("effects", True):
            canvas.itemconfig(forgot_text, fill="#ffffff")
        root.config(cursor="")

    for item in (login_btn, login_text):
        canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
        canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))
        canvas.tag_bind(item, "<Button-1>", do_login)

    canvas.tag_bind(forgot_text, "<Enter>", forgot_enter)
    canvas.tag_bind(forgot_text, "<Leave>", forgot_leave)
    canvas.tag_bind(forgot_text, "<Button-1>", lambda e: show_forgot_password())

    username_entry.bind("<Return>", do_login)
    password_entry.bind("<Return>", do_login)


def show_forgot_password():
    global current_page
    clear_entries()
    current_page = "forgot"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    accent = theme["accent"]

    width = root.winfo_width()
    height = root.winfo_height()

    draw_login_background(width, height)

    canvas.create_text(width // 2, 120, text="استرجاع كلمة السر",
                       fill="white", font=("Arial", fonts["title"] - 12, "bold"))

    canvas.create_text(width // 2, 260, text="بيانات الدخول الافتراضية عند إعادة الضبط:",
                       fill="white", font=("Arial", fonts["subtitle"], "bold"))

    canvas.create_text(width // 2, 320, text="اسم المستخدم: admin",
                       fill="#dddddd", font=("Arial", fonts["normal"] + 4))

    canvas.create_text(width // 2, 365, text="كلمة المرور: 1234",
                       fill="#dddddd", font=("Arial", fonts["normal"] + 4))

    reset_btn = canvas.create_rectangle(width // 2 - 170, 440, width // 2 + 170, 500,
                                        fill=accent, outline=accent, width=3)

    reset_text = canvas.create_text(width // 2, 470, text="إعادة ضبط الدخول",
                                    fill="black", font=("Arial", fonts["button"] + 2, "bold"))

    def reset_click(event):
        settings["username"] = "admin"
        settings["password"] = "1234"
        save_settings(settings)
        messagebox.showinfo("تم", "تمت إعادة ضبط بيانات الدخول.")
        show_login()

    for item in (reset_btn, reset_text):
        canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
        canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))
        canvas.tag_bind(item, "<Button-1>", reset_click)

    draw_back_button(show_login)


def show_home():
    global current_page, normal_icons, large_icons
    clear_entries()
    current_page = "home"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_background(width, height)

    canvas.create_text(width // 2, int(height * 0.12), text="HAMZA SERVICES",
                       fill=theme["text"], font=("Arial", fonts["title"], "bold"))

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

        text_id = canvas.create_text(x, text_y, text=label,
                                     fill=theme["text"],
                                     font=("Arial", fonts["menu"], "bold"),
                                     justify="center")

        def on_enter(event, k=key, img=image_id):
            if settings.get("effects", True):
                canvas.itemconfig(img, image=large_icons[k])
            root.config(cursor="hand2")

        def on_leave(event, k=key, img=image_id):
            if settings.get("effects", True):
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
    clear_entries()
    current_page = "settings"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("الإعدادات", show_home)

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

    def click_setting(k):
        if k == "customize":
            show_customize()
        elif k == "account":
            show_account_security()
        elif k == "printer":
            show_printer_settings()
        elif k == "clients_db":
            show_clients_database()
        else:
            show_setting_placeholder(k)

    draw_list(settings_items, click_setting)


def show_printer_settings():
    global current_page
    clear_entries()
    current_page = "printer"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("الطباعة", show_settings)

    color_status = "ملونة" if settings.get("color_printing", True) else "أبيض وأسود"
    preview_status = "مفعلة" if settings.get("print_preview", True) else "معطلة"
    pdf_status = "مفعل" if settings.get("save_pdf", True) else "معطل"

    printer_items = [
        ("🖨", "#2f7df6", "اختيار الطابعة", f"الطابعة الحالية: {settings.get('printer_name', 'الطابعة الافتراضية')}", "printer_name"),
        ("🎨", "#8d3ff2", "الطباعة الملونة / أبيض وأسود", f"الوضع الحالي: {color_status}", "color_printing"),
        ("👁", "#22c55e", "معاينة قبل الطباعة", f"الحالة الحالية: {preview_status}", "print_preview"),
        ("💾", "#ff8a18", "حفظ كـ PDF", f"الحالة الحالية: {pdf_status}", "save_pdf"),
    ]

    def click_printer(k):
        if k == "printer_name":
            show_printer_name_form()
        elif k == "color_printing":
            toggle_color_printing()
        elif k == "print_preview":
            toggle_print_preview()
        elif k == "save_pdf":
            toggle_save_pdf()

    draw_list(printer_items, click_printer)


def show_printer_name_form():
    global current_page
    clear_entries()
    current_page = "printer_name"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("اختيار الطابعة", show_printer_settings)

    canvas.create_text(
        width // 2,
        220,
        text="اكتب اسم الطابعة التي تريد اعتمادها",
        fill=theme["text"],
        font=("Arial", fonts["subtitle"], "bold")
    )

    canvas.create_text(
        width // 2,
        265,
        text=f"الحالية: {settings.get('printer_name', 'الطابعة الافتراضية')}",
        fill=theme["muted"],
        font=("Arial", fonts["normal"] + 2)
    )

    entry = tk.Entry(root, font=("Arial", fonts["normal"] + 2), justify="center", bd=0)
    entry.insert(0, settings.get("printer_name", "الطابعة الافتراضية"))
    entry_widgets.append(entry)
    canvas.create_window(width // 2, 340, window=entry, width=430, height=45)

    def save_printer():
        value = entry.get().strip()
        if not value:
            messagebox.showerror("خطأ", "اكتب اسم الطابعة.")
            return

        settings["printer_name"] = value
        save_settings(settings)
        messagebox.showinfo("تم", "تم حفظ اسم الطابعة.")
        show_printer_settings()

    draw_save_button("حفظ الطابعة", 410, save_printer)


def show_customize():
    global current_page
    clear_entries()
    current_page = "customize"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("تخصيص الواجهة", show_settings)

    current_theme = "الوضع الفاتح" if settings.get("theme") == "light" else "الوضع الليلي"
    current_font = {"small": "صغير", "medium": "متوسط", "large": "كبير"}.get(settings.get("font_size"), "متوسط")
    effects_status = "مفعلة" if settings.get("effects", True) else "معطلة"

    customize_items = [
        ("🖼", "#2f7df6", "تغيير صورة الخلفية", "اختر صورة من الحاسوب واستعملها كخلفية للبرنامج", "change_bg"),
        ("🌙", "#8d3ff2", "الوضع الليلي / الفاتح", f"الوضع الحالي: {current_theme}", "toggle_theme"),
        ("🎨", get_accent(), "اللون الرئيسي", "اختيار لون الأزرار والعناصر النشطة داخل البرنامج", "accent_color"),
        ("🔠", "#22c55e", "حجم الخط", f"الحجم الحالي: {current_font}", "font_size"),
        ("✨", "#facc15", "التأثيرات البصرية", f"الحالة الحالية: {'مفعلة' if settings.get('effects', True) else 'معطلة'}", "effects"),
        ("♻", "#ff8a18", "إعادة ضبط المصنع", "إرجاع إعدادات الواجهة إلى الوضع الافتراضي دون حذف البيانات", "factory_reset"),
    ]

    def click_customize(k):
        if k == "change_bg":
            change_background()
        elif k == "toggle_theme":
            set_theme("light" if settings.get("theme") == "dark" else "dark")
        elif k == "accent_color":
            show_accent_colors()
        elif k == "font_size":
            show_font_sizes()
        elif k == "effects":
            toggle_effects()
        elif k == "factory_reset":
            reset_factory()

    draw_list(customize_items, click_customize)


def show_accent_colors():
    global current_page
    clear_entries()
    current_page = "accent_colors"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("اللون الرئيسي", show_customize)

    canvas.create_text(width // 2, 145, text="اختر اللون الذي يناسب واجهة البرنامج",
                       fill=theme["muted"], font=("Arial", fonts["subtitle"], "bold"))

    start_y = 215
    row_h = 70
    x1 = int(width * 0.25)
    x2 = int(width * 0.75)

    for index, (name, color) in enumerate(ACCENT_COLORS.items()):
        y1 = start_y + index * (row_h + 10)
        y2 = y1 + row_h

        card = canvas.create_rectangle(x1, y1, x2, y2,
                                       fill=theme["card"], outline=theme["border"], width=1)

        color_box = canvas.create_rectangle(x1 + 25, y1 + 15, x1 + 75, y1 + 55,
                                            fill=color, outline=color)

        selected = "  ✓" if settings.get("accent_color") == color else ""

        text = canvas.create_text(x1 + 105, y1 + 35, text=name + selected,
                                  fill=theme["text"],
                                  font=("Arial", fonts["button"] + 2, "bold"),
                                  anchor="w")

        arrow = canvas.create_text(x2 - 35, y1 + 35, text="›",
                                   fill=theme["muted"], font=("Arial", 38, "bold"))

        def enter(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card_hover"])
            root.config(cursor="hand2")

        def leave(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card"])
            root.config(cursor="")

        def click(event, chosen=color):
            set_accent_color(chosen)

        for item in (card, color_box, text, arrow):
            canvas.tag_bind(item, "<Enter>", enter)
            canvas.tag_bind(item, "<Leave>", leave)
            canvas.tag_bind(item, "<Button-1>", click)


def show_font_sizes():
    global current_page
    clear_entries()
    current_page = "font_sizes"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("حجم الخط", show_customize)

    canvas.create_text(width // 2, 145, text="اختر حجم الخط المناسب للواجهة",
                       fill=theme["muted"], font=("Arial", fonts["subtitle"], "bold"))

    sizes = [("صغير", "small"), ("متوسط", "medium"), ("كبير", "large")]
    start_y = 240
    row_h = 80
    x1 = int(width * 0.25)
    x2 = int(width * 0.75)

    for index, (label, value) in enumerate(sizes):
        y1 = start_y + index * (row_h + 12)
        y2 = y1 + row_h

        card = canvas.create_rectangle(x1, y1, x2, y2,
                                       fill=theme["card"], outline=theme["border"], width=1)

        selected = "  ✓" if settings.get("font_size") == value else ""

        text = canvas.create_text(width // 2, y1 + 40, text=label + selected,
                                  fill=theme["text"], font=("Arial", fonts["menu"], "bold"))

        def enter(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card_hover"])
            root.config(cursor="hand2")

        def leave(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card"])
            root.config(cursor="")

        def click(event, v=value):
            set_font_size(v)

        for item in (card, text):
            canvas.tag_bind(item, "<Enter>", enter)
            canvas.tag_bind(item, "<Leave>", leave)
            canvas.tag_bind(item, "<Button-1>", click)


def show_account_security():
    global current_page
    clear_entries()
    current_page = "account"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("الحساب والأمان", show_settings)

    account_items = [
        ("👤", "#2f7df6", "تغيير اسم المستخدم", "تعديل اسم المستخدم الذي تستعمله للدخول إلى البرنامج", "change_username"),
        ("🔑", "#8d3ff2", "تغيير كلمة المرور", "تحديث كلمة مرور الدخول وحماية البرنامج", "change_password"),
        ("🔒", "#55b72c", "قفل البرنامج", "إغلاق الوصول إلى البرنامج حتى يتم إدخال كلمة المرور", "lock_app"),
        ("♻", "#ff8a18", "إعادة ضبط بيانات الدخول", "إرجاع اسم المستخدم وكلمة المرور إلى القيم الافتراضية", "reset_login"),
    ]

    draw_list(account_items, lambda k: show_account_form(k))


def draw_save_button(text, y, command):
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()

    btn = canvas.create_rectangle(width // 2 - 130, y, width // 2 + 130, y + 55,
                                  fill=theme["accent"], outline=theme["accent"])

    txt = canvas.create_text(width // 2, y + 28, text=text,
                             fill="black", font=("Arial", fonts["button"], "bold"))

    def click(event):
        command()

    for item in (btn, txt):
        canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
        canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))
        canvas.tag_bind(item, "<Button-1>", click)


def show_account_form(key):
    global current_page, settings
    clear_entries()
    current_page = key
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)

    titles = {
        "change_username": "تغيير اسم المستخدم",
        "change_password": "تغيير كلمة المرور",
        "lock_app": "قفل البرنامج",
        "reset_login": "إعادة ضبط بيانات الدخول",
    }

    draw_top_back(titles.get(key, "الحساب والأمان"), show_account_security)

    if key == "change_username":
        canvas.create_text(width // 2, 210, text="اسم المستخدم الحالي:",
                           fill=theme["muted"], font=("Arial", fonts["normal"] + 2, "bold"))

        canvas.create_text(width // 2, 245, text=settings["username"],
                           fill=theme["text"], font=("Arial", fonts["subtitle"] + 2, "bold"))

        entry = tk.Entry(root, font=("Arial", fonts["normal"] + 2), justify="center", bd=0)
        entry_widgets.append(entry)
        canvas.create_window(width // 2, 330, window=entry, width=360, height=45)

        def save_username():
            value = entry.get().strip()
            if not value:
                messagebox.showerror("خطأ", "اكتب اسم مستخدم جديد.")
                return
            settings["username"] = value
            save_settings(settings)
            messagebox.showinfo("تم", "تم تغيير اسم المستخدم بنجاح.")
            show_account_security()

        draw_save_button("حفظ اسم المستخدم", 395, save_username)

    elif key == "change_password":
        old_entry = tk.Entry(root, font=("Arial", fonts["normal"]), justify="center", show="*", bd=0)
        new_entry = tk.Entry(root, font=("Arial", fonts["normal"]), justify="center", show="*", bd=0)
        confirm_entry = tk.Entry(root, font=("Arial", fonts["normal"]), justify="center", show="*", bd=0)

        entry_widgets.extend([old_entry, new_entry, confirm_entry])

        canvas.create_text(width // 2, 190, text="كلمة المرور الحالية",
                           fill=theme["text"], font=("Arial", fonts["normal"], "bold"))
        canvas.create_window(width // 2, 230, window=old_entry, width=360, height=42)

        canvas.create_text(width // 2, 285, text="كلمة المرور الجديدة",
                           fill=theme["text"], font=("Arial", fonts["normal"], "bold"))
        canvas.create_window(width // 2, 325, window=new_entry, width=360, height=42)

        canvas.create_text(width // 2, 380, text="تأكيد كلمة المرور الجديدة",
                           fill=theme["text"], font=("Arial", fonts["normal"], "bold"))
        canvas.create_window(width // 2, 420, window=confirm_entry, width=360, height=42)

        def save_password():
            old = old_entry.get()
            new = new_entry.get()
            confirm = confirm_entry.get()

            if old != settings["password"]:
                messagebox.showerror("خطأ", "كلمة المرور الحالية غير صحيحة.")
                return
            if len(new) < 4:
                messagebox.showerror("خطأ", "كلمة المرور يجب أن تكون 4 أحرف أو أكثر.")
                return
            if new != confirm:
                messagebox.showerror("خطأ", "كلمة المرور الجديدة غير متطابقة.")
                return

            settings["password"] = new
            save_settings(settings)
            messagebox.showinfo("تم", "تم تغيير كلمة المرور بنجاح.")
            show_account_security()

        draw_save_button("حفظ كلمة المرور", 485, save_password)

    elif key == "reset_login":
        canvas.create_text(width // 2, 250, text="سيتم إرجاع بيانات الدخول إلى:",
                           fill=theme["text"], font=("Arial", fonts["subtitle"], "bold"))

        canvas.create_text(width // 2, 305, text="اسم المستخدم: admin",
                           fill=theme["muted"], font=("Arial", fonts["normal"] + 4))

        canvas.create_text(width // 2, 345, text="كلمة المرور: 1234",
                           fill=theme["muted"], font=("Arial", fonts["normal"] + 4))

        def reset_login():
            settings["username"] = "admin"
            settings["password"] = "1234"
            save_settings(settings)
            messagebox.showinfo("تم", "تمت إعادة ضبط بيانات الدخول.")
            show_account_security()

        draw_save_button("إعادة الضبط", 420, reset_login)

    elif key == "lock_app":
        canvas.create_text(width // 2, 270, text="تم قفل البرنامج.",
                           fill=theme["text"], font=("Arial", fonts["subtitle"] + 2, "bold"))

        canvas.create_text(width // 2, 320, text="سيتم الرجوع إلى شاشة تسجيل الدخول.",
                           fill=theme["muted"], font=("Arial", fonts["normal"] + 2))

        root.after(1000, show_login)



def show_clients_database():
    global current_page
    clear_entries()
    current_page = "clients_db"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("قاعدة بيانات الزبائن", show_settings)

    clients_count = settings.get("clients_count", 0)

    clients_items = [
        ("➕", "#2f7df6", "إضافة زبون", "إدخال زبون جديد إلى قاعدة البيانات", "add_client"),
        ("👥", "#8d3ff2", "قائمة الزبائن", f"عدد الزبائن المسجلين حاليًا: {clients_count}", "clients_list"),
        ("🔍", "#22c55e", "البحث عن زبون", "البحث السريع بالاسم أو الهاتف أو رقم الوثيقة", "search_client"),
        ("✏", "#ff8a18", "تعديل بيانات زبون", "تحديث معلومات زبون موجود في قاعدة البيانات", "edit_client"),
        ("🗑", "#ef4444", "حذف زبون", "حذف زبون من قاعدة البيانات بعد التأكيد", "delete_client"),
        ("📄", "#25b7b1", "تصدير بيانات", "تصدير قائمة الزبائن لاحقًا إلى ملف خارجي", "export_clients"),
        ("📊", "#facc15", "إحصائيات الزبائن", "عرض عدد الزبائن والنشاطات المرتبطة بهم", "clients_stats"),
    ]

    def click_clients(k):
        if k == "add_client":
            show_add_client_form()
        elif k == "clients_list":
            show_clients_list()
        elif k == "search_client":
            show_search_client()
        elif k == "edit_client":
            show_edit_client_select()
        elif k == "delete_client":
            show_delete_client_select()
        elif k == "clients_stats":
            show_clients_stats()
        else:
            show_clients_placeholder(k)

    draw_list(clients_items, click_clients)



def show_add_client_form():
    global current_page, clients_data
    clear_entries()
    current_page = "add_client"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("إضافة زبون", show_clients_database)

    fields = [
        ("الاسم الكامل", 185),
        ("رقم الهاتف", 275),
        ("العنوان", 365),
        ("ملاحظات", 455),
    ]

    entries = {}

    for label, y in fields:
        canvas.create_text(
            width // 2,
            y,
            text=label,
            fill=theme["text"],
            font=("Arial", fonts["normal"], "bold")
        )

        entry = tk.Entry(
            root,
            font=("Arial", fonts["normal"]),
            justify="center",
            bd=0
        )

        entry_widgets.append(entry)
        entries[label] = entry

        canvas.create_window(
            width // 2,
            y + 40,
            window=entry,
            width=460,
            height=42
        )

    def save_client():
        full_name = entries["الاسم الكامل"].get().strip()
        phone = entries["رقم الهاتف"].get().strip()
        address = entries["العنوان"].get().strip()
        notes = entries["ملاحظات"].get().strip()

        if not full_name:
            messagebox.showerror("خطأ", "اكتب اسم الزبون.")
            return

        client = {
            "id": len(clients_data) + 1,
            "full_name": full_name,
            "phone": phone,
            "address": address,
            "notes": notes
        }

        clients_data.append(client)
        save_clients(clients_data)
        refresh_clients_count()

        messagebox.showinfo("تم", "تمت إضافة الزبون بنجاح.")
        show_clients_database()

    draw_save_button("حفظ الزبون", 545, save_client)


def show_clients_list():
    global current_page
    clear_entries()
    current_page = "clients_list"
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("قائمة الزبائن", show_clients_database)

    if not clients_data:
        canvas.create_text(
            width // 2,
            300,
            text="لا يوجد زبائن مسجلون حاليًا.",
            fill=theme["muted"],
            font=("Arial", fonts["subtitle"], "bold")
        )
        return

    x1 = int(width * 0.10)
    x2 = int(width * 0.90)
    start_y = 140
    row_h = 72
    gap = 8

    visible_clients = clients_data[-6:]

    for index, client in enumerate(visible_clients):
        y1 = start_y + index * (row_h + gap)
        y2 = y1 + row_h

        card = canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=theme["card"],
            outline=theme["border"],
            width=1
        )

        icon_bg = canvas.create_rectangle(
            x1 + 25,
            y1 + 12,
            x1 + 75,
            y1 + 60,
            fill="#8d3ff2",
            outline="#8d3ff2"
        )

        canvas.create_text(
            x1 + 50,
            y1 + 36,
            text="👤",
            fill="white",
            font=("Arial", 21, "bold")
        )

        canvas.create_text(
            x1 + 105,
            y1 + 24,
            text=client.get("full_name", ""),
            fill=theme["text"],
            font=("Arial", fonts["button"], "bold"),
            anchor="w"
        )

        info = f"الهاتف: {client.get('phone', '')}   |   العنوان: {client.get('address', '')}"

        canvas.create_text(
            x1 + 105,
            y1 + 52,
            text=info,
            fill=theme["muted"],
            font=("Arial", fonts["small"]),
            anchor="w"
        )

        def enter(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card_hover"])
            root.config(cursor="hand2")

        def leave(event, c=card):
            if settings.get("effects", True):
                canvas.itemconfig(c, fill=theme["card"])
            root.config(cursor="")

        canvas.tag_bind(card, "<Enter>", enter)
        canvas.tag_bind(card, "<Leave>", leave)

    canvas.create_text(
        width // 2,
        height - 40,
        text=f"عدد الزبائن المسجلين: {len(clients_data)}",
        fill=theme["muted"],
        font=("Arial", fonts["small"] + 1)
    )

def draw_client_card(client, y1, action_text="", action_command=None):
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    x1 = int(width * 0.10)
    x2 = int(width * 0.90)
    y2 = y1 + 72

    card = canvas.create_rectangle(x1, y1, x2, y2, fill=theme["card"], outline=theme["border"], width=1)
    icon_bg = canvas.create_rectangle(x1 + 25, y1 + 12, x1 + 75, y1 + 60, fill="#8d3ff2", outline="#8d3ff2")
    icon = canvas.create_text(x1 + 50, y1 + 36, text="👤", fill="white", font=("Arial", 21, "bold"))
    name_text = canvas.create_text(x1 + 105, y1 + 24, text=client.get("full_name", ""), fill=theme["text"], font=("Arial", fonts["button"], "bold"), anchor="w")
    info = f"الهاتف: {client.get('phone', '')}   |   العنوان: {client.get('address', '')}"
    info_text = canvas.create_text(x1 + 105, y1 + 52, text=info, fill=theme["muted"], font=("Arial", fonts["small"]), anchor="w")
    items = [card, icon_bg, icon, name_text, info_text]

    if action_text and action_command:
        action_btn = canvas.create_rectangle(x2 - 160, y1 + 18, x2 - 35, y1 + 54, fill=theme["accent"], outline=theme["accent"], width=1)
        action_label = canvas.create_text(x2 - 98, y1 + 36, text=action_text, fill="black", font=("Arial", fonts["small"] + 2, "bold"))
        items.extend([action_btn, action_label])
        def action_click(event, c=client):
            action_command(c)
        for item in (action_btn, action_label):
            canvas.tag_bind(item, "<Button-1>", action_click)

    def enter(event):
        if settings.get("effects", True):
            canvas.itemconfig(card, fill=theme["card_hover"])
        root.config(cursor="hand2")

    def leave(event):
        if settings.get("effects", True):
            canvas.itemconfig(card, fill=theme["card"])
        root.config(cursor="")

    for item in items:
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)


def show_search_client():
    global current_page
    clear_entries()
    current_page = "search_client"
    canvas.delete("all")
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)
    draw_top_back("البحث عن زبون", show_clients_database)

    canvas.create_text(width // 2, 180, text="اكتب الاسم أو رقم الهاتف أو العنوان", fill=theme["text"], font=("Arial", fonts["subtitle"], "bold"))
    search_entry = tk.Entry(root, font=("Arial", fonts["normal"] + 2), justify="center", bd=0)
    entry_widgets.append(search_entry)
    canvas.create_window(width // 2, 235, window=search_entry, width=470, height=45)

    def perform_search(event=None):
        query = search_entry.get().strip().lower()
        clear_entries()
        canvas.delete("all")
        draw_background(width, height)
        draw_top_back("نتائج البحث", show_clients_database)

        if not query:
            canvas.create_text(width // 2, 300, text="اكتب كلمة للبحث.", fill=theme["muted"], font=("Arial", fonts["subtitle"], "bold"))
            return

        results = []
        for client in clients_data:
            text = " ".join([str(client.get("full_name", "")), str(client.get("phone", "")), str(client.get("address", "")), str(client.get("notes", ""))]).lower()
            if query in text:
                results.append(client)

        if not results:
            canvas.create_text(width // 2, 300, text="لم يتم العثور على زبون مطابق.", fill=theme["muted"], font=("Arial", fonts["subtitle"], "bold"))
            return

        canvas.create_text(width // 2, 135, text=f"عدد النتائج: {len(results)}", fill=theme["muted"], font=("Arial", fonts["normal"], "bold"))
        for index, client in enumerate(results[:6]):
            draw_client_card(client, 175 + index * 82)

    draw_save_button("بحث", 300, perform_search)
    search_entry.bind("<Return>", perform_search)


def show_edit_client_select():
    global current_page
    clear_entries()
    current_page = "edit_client"
    canvas.delete("all")
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)
    draw_top_back("تعديل بيانات زبون", show_clients_database)

    if not clients_data:
        canvas.create_text(width // 2, 300, text="لا يوجد زبائن لتعديلهم.", fill=theme["muted"], font=("Arial", fonts["subtitle"], "bold"))
        return

    canvas.create_text(width // 2, 135, text="اختر الزبون الذي تريد تعديل بياناته", fill=theme["muted"], font=("Arial", fonts["normal"], "bold"))
    for index, client in enumerate(clients_data[-6:]):
        draw_client_card(client, 170 + index * 82, "تعديل", show_edit_client_form)


def show_edit_client_form(client):
    global current_page
    clear_entries()
    current_page = "edit_client_form"
    canvas.delete("all")
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)
    draw_top_back("تعديل بيانات زبون", show_edit_client_select)

    fields = [("الاسم الكامل", "full_name", 185), ("رقم الهاتف", "phone", 275), ("العنوان", "address", 365), ("ملاحظات", "notes", 455)]
    entries = {}
    for label, field_key, y in fields:
        canvas.create_text(width // 2, y, text=label, fill=theme["text"], font=("Arial", fonts["normal"], "bold"))
        entry = tk.Entry(root, font=("Arial", fonts["normal"]), justify="center", bd=0)
        entry.insert(0, client.get(field_key, ""))
        entry_widgets.append(entry)
        entries[field_key] = entry
        canvas.create_window(width // 2, y + 40, window=entry, width=460, height=42)

    def save_edit():
        full_name = entries["full_name"].get().strip()
        if not full_name:
            messagebox.showerror("خطأ", "اسم الزبون لا يمكن أن يكون فارغًا.")
            return
        for item in clients_data:
            if item.get("id") == client.get("id"):
                item["full_name"] = full_name
                item["phone"] = entries["phone"].get().strip()
                item["address"] = entries["address"].get().strip()
                item["notes"] = entries["notes"].get().strip()
                break
        save_clients(clients_data)
        refresh_clients_count()
        messagebox.showinfo("تم", "تم تعديل بيانات الزبون بنجاح.")
        show_clients_database()

    draw_save_button("حفظ التعديل", 545, save_edit)


def show_delete_client_select():
    global current_page
    clear_entries()
    current_page = "delete_client"
    canvas.delete("all")
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)
    draw_top_back("حذف زبون", show_clients_database)

    if not clients_data:
        canvas.create_text(width // 2, 300, text="لا يوجد زبائن لحذفهم.", fill=theme["muted"], font=("Arial", fonts["subtitle"], "bold"))
        return

    canvas.create_text(width // 2, 135, text="اختر الزبون الذي تريد حذفه", fill=theme["muted"], font=("Arial", fonts["normal"], "bold"))
    for index, client in enumerate(clients_data[-6:]):
        draw_client_card(client, 170 + index * 82, "حذف", delete_client)


def delete_client(client):
    answer = messagebox.askyesno("تأكيد الحذف", f"هل تريد حذف الزبون: {client.get('full_name', '')}؟")
    if not answer:
        return
    global clients_data
    clients_data = [item for item in clients_data if item.get("id") != client.get("id")]
    save_clients(clients_data)
    refresh_clients_count()
    messagebox.showinfo("تم", "تم حذف الزبون بنجاح.")
    show_clients_database()


def show_clients_stats():
    global current_page
    clear_entries()
    current_page = "clients_stats"
    canvas.delete("all")
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()
    draw_background(width, height)
    draw_top_back("إحصائيات الزبائن", show_clients_database)

    total = len(clients_data)
    with_phone = len([c for c in clients_data if c.get("phone", "").strip()])
    with_address = len([c for c in clients_data if c.get("address", "").strip()])
    stats_items = [("👥", "#2f7df6", "عدد الزبائن", str(total)), ("📞", "#22c55e", "زبائن لديهم رقم هاتف", str(with_phone)), ("🏠", "#8d3ff2", "زبائن لديهم عنوان", str(with_address))]

    start_y = 190
    x1 = int(width * 0.20)
    x2 = int(width * 0.80)
    row_h = 82
    gap = 14
    for index, (symbol, color, label, value) in enumerate(stats_items):
        y1 = start_y + index * (row_h + gap)
        y2 = y1 + row_h
        canvas.create_rectangle(x1, y1, x2, y2, fill=theme["card"], outline=theme["border"], width=1)
        canvas.create_rectangle(x1 + 25, y1 + 15, x1 + 80, y1 + 67, fill=color, outline=color)
        canvas.create_text(x1 + 52, y1 + 41, text=symbol, fill="white", font=("Arial", 23, "bold"))
        canvas.create_text(x1 + 115, y1 + 28, text=label, fill=theme["text"], font=("Arial", fonts["button"], "bold"), anchor="w")
        canvas.create_text(x1 + 115, y1 + 58, text=value, fill=theme["muted"], font=("Arial", fonts["normal"]), anchor="w")


def show_clients_placeholder(key):
    global current_page
    clear_entries()
    current_page = key
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)

    titles = {
        "add_client": "إضافة زبون",
        "clients_list": "قائمة الزبائن",
        "search_client": "البحث عن زبون",
        "edit_client": "تعديل بيانات زبون",
        "delete_client": "حذف زبون",
        "export_clients": "تصدير بيانات",
        "clients_stats": "إحصائيات الزبائن",
    }

    draw_top_back(titles.get(key, "قاعدة بيانات الزبائن"), show_clients_database)

    canvas.create_text(
        width // 2,
        270,
        text="سنقوم ببناء هذه الوظيفة لاحقًا.",
        fill=theme["muted"],
        font=("Arial", fonts["subtitle"], "bold")
    )

def show_setting_placeholder(key):
    global current_page
    clear_entries()
    current_page = key
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)

    titles = {
        "documents_settings": "إدارة الوثائق",
        "backup": "النسخ الاحتياطي والحماية",
        "clients_db": "قاعدة بيانات الزبائن",
        "smart": "الذكاء والسرعة",
        "info": "معلومات البرنامج",
    }

    title = titles.get(key, "قسم الإعدادات")
    draw_top_back(title, show_settings)

    if key == "info":
        info_items = [
            ("📦", "#2f7df6", "اسم البرنامج", "HAMZA SERVICES"),
            ("⚙", "#8d3ff2", "الإصدار", "Version 1.0"),
            ("👨‍💻", "#22c55e", "المطور", "Hamza"),
            ("🖥", "#ff8a18", "نوع البرنامج", "إدارة وخدمات مكتبية"),
            ("🛡", "#25b7b1", "الحالة", "مستقر ويعمل بشكل جيد"),
            ("✨", "#facc15", "الواجهة", "واجهة حديثة قابلة للتخصيص"),
        ]

        start_y = 150
        row_h = 78
        gap = 10
        x1 = int(width * 0.15)
        x2 = int(width * 0.85)

        for index, (symbol, color, label, value) in enumerate(info_items):
            y1 = start_y + index * (row_h + gap)
            y2 = y1 + row_h

            card = canvas.create_rectangle(x1, y1, x2, y2,
                                           fill=theme["card"],
                                           outline=theme["border"],
                                           width=1)

            icon_bg = canvas.create_rectangle(x1 + 25, y1 + 14, x1 + 78, y1 + 64,
                                              fill=color, outline=color)

            icon_text = canvas.create_text(x1 + 51, y1 + 39, text=symbol,
                                           fill="white",
                                           font=("Arial", 22, "bold"))

            title_text = canvas.create_text(x1 + 110, y1 + 25, text=label,
                                            fill=theme["text"],
                                            font=("Arial", fonts["button"] + 1, "bold"),
                                            anchor="w")

            value_text = canvas.create_text(x1 + 110, y1 + 53, text=value,
                                            fill=theme["muted"],
                                            font=("Arial", fonts["normal"]),
                                            anchor="w")

            def enter(event, c=card):
                if settings.get("effects", True):
                    canvas.itemconfig(c, fill=theme["card_hover"])
                root.config(cursor="hand2")

            def leave(event, c=card):
                if settings.get("effects", True):
                    canvas.itemconfig(c, fill=theme["card"])
                root.config(cursor="")

            for item in (card, icon_bg, icon_text, title_text, value_text):
                canvas.tag_bind(item, "<Enter>", enter)
                canvas.tag_bind(item, "<Leave>", leave)

        canvas.create_text(width // 2, height - 40, text="HAMZA SERVICES © 2026",
                           fill=theme["muted"], font=("Arial", fonts["small"] + 1))

        return

    canvas.create_text(width // 2, 300,
                       text="سنقوم ببناء هذا القسم لاحقًا.",
                       fill=theme["muted"],
                       font=("Arial", fonts["subtitle"], "bold"))


def show_placeholder(section):
    global current_page
    clear_entries()
    current_page = section
    canvas.delete("all")

    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)

    titles = {
        "documents": "واجهة الوثائق",
        "electronic": "واجهة الخدمات الإلكترونية",
        "archive": "واجهة الأرشيف",
    }

    canvas.create_text(width // 2, 140, text=titles.get(section, "واجهة جديدة"),
                       fill=theme["text"], font=("Arial", fonts["title"] - 6, "bold"))

    canvas.create_text(width // 2, 320, text="هذه واجهة مؤقتة، سنبني تفاصيلها لاحقًا.",
                       fill=theme["muted"], font=("Arial", fonts["subtitle"], "bold"))

    draw_back_button(show_home)


def draw_back_button(command):
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()
    height = root.winfo_height()

    btn = canvas.create_rectangle(width // 2 - 90, height - 82,
                                  width // 2 + 90, height - 32,
                                  fill=theme["button"],
                                  outline=theme["border"],
                                  width=1)

    txt = canvas.create_text(width // 2, height - 57, text="رجوع",
                             fill=theme["text"],
                             font=("Arial", fonts["button"], "bold"))

    def enter(event):
        if settings.get("effects", True):
            canvas.itemconfig(btn, fill=theme["button_hover"])
        root.config(cursor="hand2")

    def leave(event):
        if settings.get("effects", True):
            canvas.itemconfig(btn, fill=theme["button"])
        root.config(cursor="")

    def click(event):
        command()

    for item in (btn, txt):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def on_resize(event):
    if event.widget == root:
        if current_page == "login":
            show_login()
        elif current_page == "forgot":
            show_forgot_password()
        elif current_page == "home":
            show_home()
        elif current_page == "settings":
            show_settings()
        elif current_page == "customize":
            show_customize()
        elif current_page == "accent_colors":
            show_accent_colors()
        elif current_page == "font_sizes":
            show_font_sizes()
        elif current_page == "account":
            show_account_security()
        elif current_page == "printer":
            show_printer_settings()
        elif current_page == "printer_name":
            show_printer_name_form()
        elif current_page in ["change_username", "change_password", "lock_app", "reset_login"]:
            show_account_form(current_page)
        elif current_page == "clients_db":
            show_clients_database()
        elif current_page == "add_client":
            show_add_client_form()
        elif current_page == "clients_list":
            show_clients_list()
        elif current_page == "search_client":
            show_search_client()
        elif current_page == "edit_client":
            show_edit_client_select()
        elif current_page == "edit_client_form":
            show_edit_client_select()
        elif current_page == "delete_client":
            show_delete_client_select()
        elif current_page == "clients_stats":
            show_clients_stats()
        elif current_page in ["export_clients"]:
            show_clients_placeholder(current_page)
        elif current_page in ["documents_settings", "backup", "smart", "info"]:
            show_setting_placeholder(current_page)
        else:
            show_placeholder(current_page)


root.bind("<Configure>", on_resize)

show_login()
root.mainloop()
