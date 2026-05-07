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

DEFAULT_SETTINGS = {
    "username": "admin",
    "password": "1234",
    "background": "",
    "theme": "dark",
    "accent_color": "#ffa51f",
    "font_size": "medium",
    "effects": True
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


def draw_top_back(title, back_command):
    theme = get_theme()
    fonts = get_fonts()
    width = root.winfo_width()

    canvas.create_text(35, 28, text="HAMZA SERVICES", fill=theme["text"],
                       font=("Arial", fonts["normal"], "bold"), anchor="w")

    back_box = canvas.create_rectangle(35, 60, 125, 105, fill=theme["button"],
                                       outline=theme["border"], width=1)

    back_text = canvas.create_text(80, 82, text="←  رجوع", fill=theme["text"],
                                   font=("Arial", fonts["normal"], "bold"))

    canvas.create_text(width // 2, 82, text=title, fill=theme["text"],
                       font=("Arial", fonts["title"] - 14, "bold"))

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

        card = canvas.create_rectangle(list_x1, y1, list_x2, y2,
                                       fill=theme["card"], outline=theme["border"], width=1)

        icon_bg = canvas.create_rectangle(list_x1 + 28, y1 + 12, list_x1 + 78, y1 + 62,
                                          fill=color, outline=color)

        icon_text = canvas.create_text(list_x1 + 53, y1 + 37, text=symbol,
                                       fill="white", font=("Arial", 23, "bold"))

        title_text = canvas.create_text(list_x1 + 115, y1 + 25, text=title,
                                        fill=theme["text"],
                                        font=("Arial", fonts["button"], "bold"),
                                        anchor="w")

        desc_text = canvas.create_text(list_x1 + 115, y1 + 52, text=desc,
                                       fill=theme["muted"],
                                       font=("Arial", fonts["small"]),
                                       anchor="w")

        arrow = canvas.create_text(list_x2 - 38, y1 + 37, text="›",
                                   fill=theme["muted"], font=("Arial", 42, "bold"))

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
        else:
            show_setting_placeholder(k)

    draw_list(settings_items, click_setting)


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
        ("✨", "#facc15", "التأثيرات البصرية", f"الحالة الحالية: {effects_status}", "effects"),
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
        "printer": "الطباعة",
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
        elif current_page in ["change_username", "change_password", "lock_app", "reset_login"]:
            show_account_form(current_page)
        elif current_page in ["printer", "documents_settings", "backup", "clients_db", "smart", "info"]:
            show_setting_placeholder(current_page)
        else:
            show_placeholder(current_page)


root.bind("<Configure>", on_resize)

show_login()
root.mainloop()
